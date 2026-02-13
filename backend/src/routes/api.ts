import { Router } from 'express';
import multer from 'multer';
import rateLimit from 'express-rate-limit';
import { analyzeCrop, getScan } from '../controllers/scanController';
import { login, register } from '../controllers/authController';
import { authenticateToken } from '../middleware/auth';
import { asyncHandler } from '../utils/asyncHandler';

const authLimiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 5, // Limit each IP to 5 requests per windowMs for auth
    message: { error: 'Too many auth attempts, please try again in an hour.' },
    standardHeaders: true,
    legacyHeaders: false,
});

const router = Router();
const upload = multer({ storage: multer.memoryStorage() });

// Public Routes
router.post('/auth/register', authLimiter, asyncHandler(register));
router.post('/auth/login', authLimiter, asyncHandler(login));

// Protected Routes
router.post('/scan', authenticateToken as any, upload.single('image'), asyncHandler(analyzeCrop));
router.get('/scan/:id', authenticateToken as any, asyncHandler(getScan));

export default router;
