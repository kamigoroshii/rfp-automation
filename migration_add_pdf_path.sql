-- Add pdf_path column to rfps table
-- Run this in your PostgreSQL database

ALTER TABLE rfps 
ADD COLUMN IF NOT EXISTS pdf_path TEXT;

-- Add index for faster lookups
CREATE INDEX IF NOT EXISTS idx_rfps_pdf_path ON rfps(pdf_path);

-- Verify the column was added
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'rfps' AND column_name = 'pdf_path';
