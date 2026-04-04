-- Create table for AI Leads
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    needs_ai BOOLEAN,
    priority_score INTEGER CHECK (priority_score >= 1 AND priority_score <= 10),
    technical_reason TEXT,
    custom_pitch TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
