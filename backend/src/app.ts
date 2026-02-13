import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { env } from './config/env';
import apiRoutes from './routes/api';
import { errorHandler } from './middleware/errorHandler';
import { setupGracefulShutdown } from './utils/shutdown';

const app = express();

// Security Middleware
app.use(helmet());
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS ? process.env.ALLOWED_ORIGINS.split(',') : '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
}));
app.use(express.json());

// Global Rate Limiting
const globalLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: { error: 'Too many requests, please try again later.' },
    standardHeaders: true,
    legacyHeaders: false,
});
app.use(globalLimiter);

// Routes
app.use('/api', apiRoutes);

// Health Check
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        environment: env.NODE_ENV,
        timestamp: new Date().toISOString()
    });
});

// Centralized Error Handling (must be after routes)
app.use(errorHandler);

const server = app.listen(env.PORT, () => {
    console.log(`🚀 Krishi-Net Server running in ${env.NODE_ENV} mode on port ${env.PORT}`);
    console.log(`🔗 ML Service URL: ${env.ML_SERVICE_URL}`);
});

// Setup Graceful Shutdown
setupGracefulShutdown(server);
