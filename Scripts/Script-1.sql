SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'staging'
AND table_name = 'deliveries'
ORDER BY ordinal_position;