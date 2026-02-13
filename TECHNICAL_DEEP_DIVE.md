# Krishi-Net: Technical Deep-Dive & Knowledge Breakdown

This document serves as an exhaustive technical guide for the Krishi-Net system, designed for high-level technical reviews, hackathon defenses, and engineering interviews.

---

## SECTION 1 — SYSTEM ARCHITECTURE OVERVIEW

### Core Architecture
Krishi-Net is built on a **Microservices-oriented Distributed Architecture**. It separates high-CPU intensive tasks (AI Inference) from standard I/O intensive tasks (User Management/Storage).

- **Mobile Client (React Native/Expo)**: The "Intelligent Edge". Handles UI rendering, camera interaction, local image processing, and state management.
- **Backend API (Node.js/Express)**: The "Orchestrator". Manages business logic, authentication, database transactions, and sanitizes communications with the ML microservice.
- **ML Microservice (Python/FastAPI)**: The "Inference Engine". A specialized service dedicated to running the TensorFlow model and processing classification requests.
- **Database (PostgreSQL/Prisma)**: The "Source of Truth". A relational database for structured scan history and user profiles.

### Request Lifecycles

#### 1. Login Lifecycle
1. **Client**: User submits credentials -> `apiClient.post('/auth/login')`.
2. **Backend**: Express receives request -> Calls `authController`.
3. **Validation**: Zod validates input schema -> Controller queries Postgres via Prisma.
4. **Auth**: Bcrypt compares hashes -> If match, JWT signed using `process.env.JWT_SECRET`.
5. **Response**: 200 OK + JWT sent to client.
6. **Client**: `SecureStore` persists JWT for subsequent requests.

#### 2. Scan Image Lifecycle
1. **Client**: Camera captures frame -> `ImageManipulator` compresses to JPEG -> `FormData` appended.
2. **Backend**: `multer` parses multipart/form-data -> `scanController` receives request.
3. **Orchestration**: Backend forwards image to `ML_SERVICE_URL` via `axios`.
4. **ML Service**: FastAPI receives file -> PIL converts to Numpy array -> TensorFlow runs `model.predict()`.
5. **Response**: ML service returns JSON (disease, confidence, treatments).
6. **Persistence**: Backend saves record to Postgres -> Returns unified response to Mobile.

---

## SECTION 2 — FRONTEND DEEP DIVE

### React Native Internals
**How it works**: React Native allows us to write JS/TS while rendering actual native UI components (UIViews on iOS, Android.Views on Android).
- **The Bridge (Legacy)**: In older versions, JS and Native communicated via asynchronous JSON serialization over a "Bridge".
- **JSI (JavaScript Interface)**: Modern RN (used in Krishi-Net) allows the JS engine to hold direct references to C++ Host Objects, enabling synchronous, high-performance communication and removing the serialization bottleneck.

### Why Expo?
- **Managed Workflow**: Standardizes the development environment, reducing "works on my machine" issues.
- **EAS (Expo Application Services)**: Provides cloud builds, making the transition from Dev to Production (APK/AAB) seamless without needing a local Android Studio/Xcode setup.

### Animations: Reanimated & Moti
**UI Thread vs JS Thread**: 
In standard React Native `Animated` API, complex animations can stutter if the JS thread is busy with business logic (API calls, state updates).
- **Reanimated Implementation**: We chose `react-native-reanimated` because it allows animations to run purely on the **UI Thread** (Main Thread). We define "Worklets" (small JS functions) that are shifted to the native side, ensuring 60fps even if the JS thread is blocked.

### Networking & Resilience
- **Axios Interceptors**: We use `apiClient.interceptors.request` to automatically inject the Bearer token from `SecureStore` into every outgoing request.
- **The 401 Handler**: If the backend returns a 401 (Unauthorized), the response interceptor automatically triggers `AuthService.logout()`, wiping the token and redirecting the user to the login flow.

### Offline Detection (NetInfo)
Using `@react-native-community/netinfo`, we monitor the `state.isConnected` flag. When the device loses connection, the `OfflineBanner` component slides down using an `Animated` transition.

### Image Optimization
**Compression Strategy**: Sending a raw 12MP camera photo (~5-8MB) to the ML service is a performance killer.
- **expo-image-manipulator**: We resize images to 1024px and reduce JPEG quality to 70%.
- **Impact**: Reduces file size by ~90% with negligible impact on AI accuracy.

---

## SECTION 3 — BACKEND DEEP DIVE

### Node.js & The Event Loop
Node.js is built on the V8 engine and the **libuv** library.
- **Single-threaded Event Loop**: Node.js handles I/O operations asynchronously. When an I/O call is made, Node registers a callback and continues.
- **Non-blocking I/O**: The "Non-blocking" nature ensures that our server can handle hundreds of concurrent requests without needing a thread-per-request model.

### Express Middleware Pipeline
We use Express because of its "unopinionated" design:
1. **Security**: `helmet` (sets secure HTTP headers) -> `cors` (restricts cross-origin access).
2. **Parsing**: `express.json()` -> `multer` for multipart images.
3. **Validation**: `express-rate-limit` -> Zod schema validation.
4. **Auth**: `authenticateToken` middleware verifies the JWT.
5. **Error Handling**: Centralized `errorHandler` catches all `next(err)` calls.

### JWT: Stateless Authentication
- **Structure**: `Header.Payload.Signature`.
- **Stateless Nature**: The server does not store "sessions" in the database. The `Payload` contains the `userId`. The `Signature` ensures the payload wasn't tampered with.
- **Scalability**: Since auth is stateless, we can spin up multiple instances of the backend on Railway without needing shared session storage.

### Prisma ORM
- **Type Safety**: Prisma generates a TypeScript client based on our `schema.prisma`. This catches database errors at compile-time.
- **Abstraction**: It allows us to write `prisma.scan.findMany()` instead of raw SQL strings.
- **Migration System**: `prisma migrate dev` ensures our production database on Railway stays in sync with our local structural changes.

---

## SECTION 4 — ML SERVICE DEEP DIVE

### FastAPI: Performance & Async
We chose FastAPI (Python) over Flask because:
- **Asynchronous by Design**: It uses the **ASGI**, allowing it to handle concurrent prediction requests without blocking the workers.
- **Pydantic Validation**: Automatically validates incoming data shapes.

### Prediction Flow Internals
1. **Reception**: Image arrives as `UploadFile`.
2. **Preprocessing**: PIL resizes the image to the exact input shape (e.g., 224x224).
3. **Normalization**: Pixel values are scaled to match the training distribution.
4. **Inference**: `model.predict(input_tensor)` is called using TensorFlow.
5. **Post-processing**: Probabilities are mapped to human-readable disease names.

### Failure Handling & Isolation
- **Microservice Separation**: If the ML service crashes due to memory exhaustion, the main Backend API remains alive.
- **Error Propagation**: The backend uses an explicit **12-second timeout** for ML requests.

---

## SECTION 5 — DATABASE & DEPLOYMENT

### PostgreSQL: Relation & ACID
- **Why Relational?**: Structured scan history (one user has many scans) naturally fits the relational model.
- **ACID Properties**: Atomicity, Consistency, Isolation, and Durability ensure that a scan is only saved if the entire transaction succeeds, preventing corrupted history logs.

### Railway: Containerized Deployment
- **Git-Ops Workflow**: Railway monitors our GitHub repo. On every push to `main`, it triggers a Nix-based build.
- **Ephemeral Storage**: Railway services are stateless. We must store persistent data in Postgres or Cloud Storage, never on the server's local disk.

### EAS Build System
- **EAS Build**: Converts our React Native code into binary executables (`.apk` or `.aab`). It handles the native build environment (Ubuntu for Android, macOS for iOS) in the cloud.
- **Signing**: EAS securely stores our Keystores and Certificates, ensuring the app can be verified by Google.

---

## SECTION 6 — SECURITY ARCHITECTURE

### Secure Token Storage
- **SecureStore vs AsyncStorage**: `AsyncStorage` is plain text. We use `expo-secure-store`, which uses **Keychain** (iOS) and **Keystore** (Android) to encrypt the JWT at rest.

### Input & File Validation
- **Zod Schema**: Every single API request (Login, Register, Scan) is validated against a Zod schema before processing.
- **Mime Filtering**: Multer is configured to only accept `image/jpeg` and `image/png`.

### Rate Limiting & DoS Protection
We implemented **Layered Rate Limiting**:
- **Global**: 100 requests / 15 mins to catch general abuse.
- **Auth Selective**: 10 requests / 15 mins for login routes.

---

## SECTION 7 — PERFORMANCE STRATEGY

### Rendering Optimizations
- **React.memo**: We use `React.memo` for list items to prevent unnecessary re-renders.
- **FlatList Tuning**: We use optimized props for smooth scrolling.

### Resource Management
- **Unmount Guards**: Using the custom `useIsMounted` hook to prevent state updates on unmounted components.

---

## SECTION 8 — TRADEOFFS & ALTERNATIVES

- **Express vs Fastify**: Chose Express for ecosystem and stability.
- **JWT vs Sessions**: Chose JWT for horizontal scalability and mobile ease.
- **PostgreSQL vs NoSQL**: Chose SQL for data integrity and ACID properties.

---

## SECTION 9 — HACKATHON DEFENSE QUESTIONS

### Architecture & System Design
1. **Q: Why a microservice for ML instead of putting it in the Node backend?**
   - **A**: Resource isolation. ML (TensorFlow) is CPU-heavy. Separating it ensures AI processing doesn't block the API event loop, and we can scale them independently.
2. **Q: How does the system handle high traffic?**
   - **A**: The stateless JWT auth allows us to scale the backend horizontally. AWS/Railway handles load balancing.
3. **Q: What happens if the Database goes down?**
   - **A**: The backend catches the Prisma error and returns a 503 error. The app shows a "Service Unavailable" toast.
4. **Q: Why use a relational database for scan history?**
   - **A**: Relational integrity. Scans are strictly tied to User IDs. ACID properties ensure history is never inconsistent.
5. **Q: How do you handle large images?**
   - **A**: We don't. We compress and resize to 1024px on the device *before* uploading to save bandwidth and speed up detection.

### Frontend (React Native/Expo)
6. **Q: What is the benefit of Reanimated over the standard Animated API?**
   - **A**: Performance. Reanimated runs purely on the UI thread, bypassing the JS bridge for 60fps animations.
7. **Q: How do you prevent memory leaks in the camera screen?**
   - **A**: We use the `useIsMounted` guard to ensure API results aren't set to state if the user navigates away mid-scan.
8. **Q: Why use SecureStore instead of AsyncStorage?**
   - **A**: Security. SecureStore encrypts the JWT using hardware-backed keystores (iOS Keychain/Android Keystore).
9. **Q: How does pull-to-refresh work on the Home Screen?**
   - **A**: It triggers a `Promise.all` call fetching weather and scan history concurrently, optimizing total fetch time.
10. **Q: How do you handle cross-platform differences?**
    - **A**: Using the `Platform` module and conditional rendering for things like notch padding and file paths.

### Backend (Node.js/Auth/API)
11. **Q: Explain the role of JWT Interceptors.**
    - **A**: They decouple networking from auth logic. The interceptor injects the token into every header automatically.
12. **Q: How do you protect against brute-force attacks?**
    - **A**: `express-rate-limit` on the `/auth` routes, limiting login attempts to 10 per 15 minutes per IP.
13. **Q: Why Zod for validation?**
    - **A**: It provides both runtime validation and TypeScript type inference, ensuring the backend logic is typed correctly.
14. **Q: What is the purpose of the 401 interceptor?**
    - **A**: Security & UX. It instantly logs out the user if the token expires on the server, preventing stale state.
15. **Q: How do you handle silent crashes in the backend?**
    - **A**: We use `uncaughtException` and `unhandledRejection` hooks for a graceful shutdown, closing DB connections properly.

### ML & Data Modeling
16. **Q: How is the ML model trained?**
    - **A**: Using Transfer Learning on MobileNetV2 with a custom dataset of 38+ plant disease classes.
17. **Q: Why is image normalization necessary?**
    - **A**: It ensures the input scale (0-255) matches the scale the model was trained on, preventing garbage feature extraction.
18. **Q: What is the accuracy of the model?**
    - **A**: Currently ~94% on the test set, with lower confidence scores for poor lighting/blurry images.
19. **Q: How do you handle low-confidence predictions?**
    - **A**: If confidence is < 60%, the app suggests retaking the photo for a better result.
20. **Q: Why use PIL instead of OpenCV in the ML service?**
    - **A**: PIL is lighter weight and specifically optimized for basic image IO and resizing in FastAPI environments.

### Security & DevOps
21. **Q: How are environment variables secured?**
    - **A**: They are injected via Railway's secret manager, never committed to Git.
22. **Q: Why use a `Procfile`?**
    - **A**: It explicitly tells the cloud environment (Railway/Heroku) exactly how to start the service reliably.
23. **Q: How do you prevent SQL injection?**
    - **A**: Prisma uses parameterized queries by default, making SQL injection via input strings virtually impossible.
24. **Q: What if someone steals a user's JWT?**
    - **A**: Without HTTPS (which we use), the token is at risk. We use secure headers to prevent Man-in-the-Middle attacks.
25. **Q: Why use `multer`? Can't we just send Base64?**
    - **A**: Base64 increases payload size by 33%. Multer handles binary multipart-form-data, which is more efficient for image transfers.

### Performance & UX
26. **Q: How do you ensure smooth scrolling in a long scan history?**
    - **A**: Memoized components and FlatList optimizations like `removeClippedSubviews`.
27. **Q: Why did you implement a custom Skeleton loader?**
    - **A**: Improved Perceived Performance. It keeps the user engaged while the network handles the API fetch.
28. **Q: How is the theme handled?**
    - **A**: A centralized `theme.ts` with a `useColorScheme` custom hook for seamless Light/Dark mode transitions.
29. **Q: What is the impact of network latency on the app?**
    - **A**: We show a "Loading Analysis" state with an animated scanner line to provide feedback during the ML round-trip.
30. **Q: How do you minimize the APK size?**
    - **A**: By using Expo's optimized packages and stripping unused assets during the EAS build process.

... [Additional 20 questions covering treatment logic, weather API, error boundaries, and future scalability] ...

*(Full list of 50 available upon request, focused on deep technical implementation details)*
