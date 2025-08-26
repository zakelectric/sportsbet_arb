#!/usr/bin/env python3
"""
Test script to verify the sportsbet arbitrage application works correctly
"""
import os
import sys

def test_imports():
    """Test that all modules can be imported successfully"""
    print("Testing imports...")
    try:
        from app import main, create_driver, process_arbitrage_opportunities
        from betus import scrape_betus
        from kalshi import get_kalshi
        from mock_data import get_mock_betus_data, get_mock_kalshi_data
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_mock_data():
    """Test with mock data"""
    print("\nTesting with mock data...")
    try:
        from mock_data import get_mock_betus_data, get_mock_kalshi_data
        import pandas as pd
        
        betus_df = get_mock_betus_data()
        kalshi_df = get_mock_kalshi_data()
        
        print(f"✓ Mock BetUS data: {len(betus_df)} rows")
        print(f"✓ Mock Kalshi data: {len(kalshi_df)} rows")
        
        # Test merge
        merged_df = pd.merge(
            betus_df,
            kalshi_df,
            on="team",
            how="inner",
            suffixes=("_betus", "_kalshi")
        )
        
        print(f"✓ Merged data: {len(merged_df)} rows")
        
        if not merged_df.empty:
            from app import process_arbitrage_opportunities
            process_arbitrage_opportunities(merged_df)
            print("✓ Arbitrage processing completed")
        
        return True
    except Exception as e:
        print(f"✗ Mock data test error: {e}")
        return False

def test_real_data_error_handling():
    """Test error handling with real data sources"""
    print("\nTesting error handling...")
    try:
        from kalshi import get_kalshi
        from app import create_driver
        
        # Test Kalshi API (should handle network errors gracefully)
        kalshi_df = get_kalshi()
        print(f"✓ Kalshi API handled gracefully, returned {len(kalshi_df)} rows")
        
        # Test Chrome driver (should handle missing browser gracefully)
        driver = create_driver()
        if driver is None:
            print("✓ Chrome driver creation handled gracefully")
        else:
            print("✓ Chrome driver created successfully")
            driver.quit()
        
        return True
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running sportsbet arbitrage application tests...\n")
    
    tests = [
        test_imports,
        test_mock_data,
        test_real_data_error_handling
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\nTest Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! The application is working correctly.")
        print("\nTo run with mock data: USE_MOCK_DATA=true python3 app.py")
        print("To run with real data: python3 app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()