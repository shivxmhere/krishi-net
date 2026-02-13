"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.scanService = void 0;
const prisma_1 = require("../lib/prisma");
const axios_1 = __importDefault(require("axios"));
const form_data_1 = __importDefault(require("form-data"));
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';
exports.scanService = {
    async analyzeCrop(imageBuffer, filename) {
        try {
            const formData = new form_data_1.default();
            formData.append('file', imageBuffer, filename);
            const response = await axios_1.default.post(`${ML_SERVICE_URL}/predict`, formData, {
                headers: {
                    ...formData.getHeaders(),
                },
                timeout: 5000,
            });
            return response.data;
        }
        catch (error) {
            console.error('ML Service Error:', error.message);
            if (error.code === 'ECONNREFUSED' || error.code === 'ECONNABORTED') {
                throw new Error('ML_SERVICE_UNAVAILABLE');
            }
            throw new Error('Analysis failed');
        }
    },
    async saveScan(data, userId) {
        try {
            return await prisma_1.prisma.scan.create({
                data: {
                    disease: data.disease,
                    confidence: data.confidence,
                    severity: data.severity,
                    treatment: data.treatment,
                    userId: userId,
                },
            });
        }
        catch (error) {
            console.error('Error saving scan:', error);
            throw new Error('Failed to save scan result');
        }
    },
    async getScanById(id) {
        try {
            return await prisma_1.prisma.scan.findUnique({
                where: { id },
            });
        }
        catch (error) {
            console.error('Error fetching scan:', error);
            throw new Error('Failed to fetch scan result');
        }
    },
};
