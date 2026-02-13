import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();

const envSchema = z.object({
    NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
    PORT: z.string().transform(Number).default(8080),
    DATABASE_URL: z.string().url(),
    JWT_SECRET: z.string().min(32, "JWT_SECRET should be at least 32 characters for production"),
    ML_SERVICE_URL: z.string().url(),
});

const result = envSchema.safeParse(process.env);

if (!result.success) {
    console.error('❌ Invalid environment variables:', result.error.format());
    process.exit(1);
}

export const env = result.data;
