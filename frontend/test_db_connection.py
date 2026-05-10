#!/usr/bin/env python3
"""
Database Connection Test Script
Run this to diagnose connection issues
"""

import psycopg2
from psycopg2 import pool

print("=" * 60)
print("DATABASE CONNECTION TEST")
print("=" * 60)

# Test 1: Direct Connection
print("\n[TEST 1] Testing direct connection...")
try:
    conn = psycopg2.connect(
        host="localhost",
        database="fyp_chatbot",
        user="postgres",
        password="123456789",
        port=5432
    )
    print("✅ Direct connection successful!")
    
    # Test query
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"   PostgreSQL version: {version[0][:50]}...")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Direct connection failed: {e}")
    exit(1)

# Test 2: Connection Pool
print("\n[TEST 2] Testing connection pool...")
try:
    test_pool = psycopg2.pool.SimpleConnectionPool(
        1,
        5,
        host="localhost",
        database="fyp_chatbot",
        user="postgres",
        password="123456789",
        port=5432
    )
    print("✅ Connection pool created successfully!")
    
    # Get connection from pool
    conn = test_pool.getconn()
    print("✅ Got connection from pool!")
    
    # Test query
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users;")
    count = cur.fetchone()[0]
    print(f"   Users table has {count} records")
    
    cur.close()
    test_pool.putconn(conn)
    print("✅ Released connection back to pool!")
    
    test_pool.closeall()
    print("✅ Closed all pool connections!")
    
except Exception as e:
    print(f"❌ Connection pool failed: {e}")
    exit(1)

# Test 3: Import db module
print("\n[TEST 3] Testing db.py module import...")
try:
    import db
    print("✅ db.py module imported successfully!")
    
    conn = db.get_connection()
    if conn:
        print("✅ Got connection from db.get_connection()!")
        
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        print(f"   Test query result: {result[0]}")
        
        cur.close()
        db.release_connection(conn)
        print("✅ Released connection successfully!")
    else:
        print("❌ db.get_connection() returned None")
        exit(1)
        
except Exception as e:
    print(f"❌ db.py module test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nYour database connection is working correctly.")
print("If your app still has issues, the problem is elsewhere.")
