-- FIRST, install the pg_vector extension
-- THEN


-- Enable the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify it's installed
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Test the vector type
SELECT '[1.0, 2.0, 3.0]'::vector AS test_vector;

-- Check available operators
SELECT
    f.opfname AS operator_family,
    c.opcname AS operator_class
FROM pg_opclass c
JOIN pg_opfamily f ON c.opcfamily = f.oid
WHERE c.opcname LIKE 'vector%';

-- 