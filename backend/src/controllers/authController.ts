import { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { z } from 'zod';
import { prisma } from '../lib/prisma';
import { env } from '../config/env';

const authSchema = z.object({
    email: z.string().email('Invalid email format'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
});

export const register = async (req: Request, res: Response) => {
    const { email, password } = authSchema.parse(req.body);

    const existingUser = await prisma.user.findUnique({ where: { email } });
    if (existingUser) {
        const err: any = new Error('User already exists');
        err.statusCode = 400;
        throw err;
    }

    const salt = await bcrypt.genSalt(10);
    const passwordHash = await bcrypt.hash(password, salt);

    const user = await prisma.user.create({
        data: {
            email,
            passwordHash,
        },
    });

    res.status(201).json({ message: 'User created successfully', userId: user.id });
};

export const login = async (req: Request, res: Response) => {
    const { email, password } = authSchema.parse(req.body);

    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) {
        const err: any = new Error('Invalid credentials');
        err.statusCode = 401;
        throw err;
    }

    const isMatch = await bcrypt.compare(password, user.passwordHash);
    if (!isMatch) {
        const err: any = new Error('Invalid credentials');
        err.statusCode = 401;
        throw err;
    }

    const token = jwt.sign({ id: user.id, email: user.email }, env.JWT_SECRET, {
        expiresIn: '7d',
    });

    res.json({ token, user: { id: user.id, email: user.email } });
};
