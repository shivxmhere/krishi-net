import { Response } from 'express';
import { AuthRequest } from '../middleware/auth';
import { scanService } from '../services/scanService';

export const analyzeCrop = async (req: AuthRequest, res: Response) => {
    if (!req.file) {
        const err: any = new Error('No image uploaded');
        err.statusCode = 400;
        throw err;
    }

    if (!req.user) {
        const err: any = new Error('Unauthorized');
        err.statusCode = 401;
        throw err;
    }

    // Call ML Service (Service handles timeouts and ML failures)
    const analysisResult = await scanService.analyzeCrop(req.file.buffer, req.file.originalname);

    // Persist to DB
    const savedScan = await scanService.saveScan(analysisResult, req.user.id);

    res.json(savedScan);
};

export const getScan = async (req: AuthRequest, res: Response) => {
    const { id } = req.params;

    if (!id) {
        const err: any = new Error('Scan ID is required');
        err.statusCode = 400;
        throw err;
    }

    const scan = await scanService.getScanById(id);

    if (!scan) {
        const err: any = new Error('Scan not found');
        err.statusCode = 404;
        throw err;
    }

    // Authorization Check: Ensure scan belongs to user
    if (scan.userId !== req.user?.id) {
        const err: any = new Error('Access denied');
        err.statusCode = 403;
        throw err;
    }

    res.json(scan);
};
