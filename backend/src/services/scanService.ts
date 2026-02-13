import { prisma } from '../lib/prisma';
import axios from 'axios';
import FormData from 'form-data';
import { env } from '../config/env';

export interface ScanData {
    disease: string;
    confidence: number;
    severity: string;
    treatment: string[];
}

export const scanService = {
    async analyzeCrop(imageBuffer: Buffer, filename: string): Promise<ScanData> {
        try {
            const formData = new FormData();
            formData.append('file', imageBuffer, filename);

            const response = await axios.post(`${env.ML_SERVICE_URL}/predict`, formData, {
                headers: {
                    ...formData.getHeaders(),
                },
                timeout: 12000, // 12s timeout for ML inference
            });

            return response.data;
        } catch (error: any) {
            console.error('[ML Service Error]:', error.message);

            if (error.code === 'ECONNREFUSED' || error.code === 'ECONNABORTED' || error.response?.status === 503) {
                const err: any = new Error('ML Service is temporarily unavailable or timed out.');
                err.statusCode = 503;
                throw err;
            }

            const err: any = new Error('Image analysis failed. Please try again with a clearer image.');
            err.statusCode = 500;
            throw err;
        }
    },

    async saveScan(data: ScanData, userId: string) {
        return await prisma.scan.create({
            data: {
                disease: data.disease,
                confidence: data.confidence,
                severity: data.severity,
                treatment: data.treatment,
                userId: userId,
            },
        });
    },

    async getScanById(id: string) {
        return await prisma.scan.findUnique({
            where: { id },
        });
    },
};
