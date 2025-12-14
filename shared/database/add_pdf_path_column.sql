-- Add pdf_path column to rfps table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='rfps' AND column_name='pdf_path'
    ) THEN
        ALTER TABLE rfps ADD COLUMN pdf_path TEXT;
        RAISE NOTICE 'Added pdf_path column to rfps table';
    ELSE
        RAISE NOTICE 'pdf_path column already exists in rfps table';
    END IF;
END $$;

-- Add index on pdf_path for faster lookups
CREATE INDEX IF NOT EXISTS idx_rfps_pdf_path ON rfps(pdf_path);

-- Display summary
SELECT 
    'rfps' as table_name,
    COUNT(*) as total_records,
    COUNT(pdf_path) as records_with_pdf,
    COUNT(*) - COUNT(pdf_path) as records_without_pdf
FROM rfps;
