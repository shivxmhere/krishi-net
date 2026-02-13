import { Server } from 'http';
import { prisma } from '../lib/prisma';

export const setupGracefulShutdown = (server: Server) => {
    const shutdown = async (signal: string) => {
        console.log(`\nReceived ${signal}. Starting graceful shutdown...`);

        // 1. Close HTTP server (stop accepting new requests)
        server.close(() => {
            console.log('HTTP server closed.');
        });

        // 2. Disconnect from Database
        try {
            await prisma.$disconnect();
            console.log('Database connection closed.');
        } catch (err) {
            console.error('Error during database disconnection:', err);
        }

        console.log('Graceful shutdown complete. Exiting.');
        process.exit(0);
    };

    // Handle signals
    process.on('SIGINT', () => shutdown('SIGINT'));
    process.on('SIGTERM', () => shutdown('SIGTERM'));

    // Handle unexpected errors
    process.on('uncaughtException', (err) => {
        console.error('Uncaught Exception:', err);
        shutdown('uncaughtException');
    });

    process.on('unhandledRejection', (reason, promise) => {
        console.error('Unhandled Rejection at:', promise, 'reason:', reason);
        shutdown('unhandledRejection');
    });
};
