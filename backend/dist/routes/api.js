"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const multer_1 = __importDefault(require("multer"));
const scanController_1 = require("../controllers/scanController");
const authController_1 = require("../controllers/authController");
const auth_1 = require("../middleware/auth");
const router = (0, express_1.Router)();
const upload = (0, multer_1.default)({ storage: multer_1.default.memoryStorage() });
// Public Routes
router.post('/auth/register', authController_1.register);
router.post('/auth/login', authController_1.login);
// Protected Routes
router.post('/scan', auth_1.authenticateToken, upload.single('image'), scanController_1.analyzeCrop);
router.get('/scan/:id', auth_1.authenticateToken, scanController_1.getScan);
exports.default = router;
