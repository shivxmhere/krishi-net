"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getScan = exports.analyzeCrop = void 0;
const scanService_1 = require("../services/scanService");
const analyzeCrop = async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No image uploaded' });
        }
        if (!req.user) {
            return res.status(401).json({ error: 'Unauthorized' });
        }
        // Call ML Service
        const analysisResult = await scanService_1.scanService.analyzeCrop(req.file.buffer, req.file.originalname);
        // Persist to DB with userId
        const savedScan = await scanService_1.scanService.saveScan(analysisResult, req.user.id);
        res.json(savedScan);
    }
    catch (error) {
        console.error('Analysis error:', error);
        if (error.message === 'ML_SERVICE_UNAVAILABLE') {
            return res.status(503).json({ error: 'ML Service is currently unavailable. Please try again later.' });
        }
        res.status(500).json({ error: 'Analysis failed' });
    }
};
exports.analyzeCrop = analyzeCrop;
const getScan = async (req, res) => {
    try {
        const { id } = req.params;
        const scan = await scanService_1.scanService.getScanById(id);
        if (!scan) {
            return res.status(404).json({ error: 'Scan not found' });
        }
        // Authorization Check: Ensure scan belongs to user
        if (scan.userId !== req.user?.id) {
            return res.status(403).json({ error: 'Access denied' });
        }
        res.json(scan);
    }
    catch (error) {
        console.error('Get scan error:', error);
        res.status(500).json({ error: 'Failed to fetch scan' });
    }
};
exports.getScan = getScan;
