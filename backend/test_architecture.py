"""
Test the architecture consistency
"""

import sys
from pathlib import Path


def test_api_structure():
    """Test that API structure is consistent"""
    print("Testing API architecture consistency...")
    
    api_path = Path("/home/mrishank/thathvamasi/backend/app/api")
    
    # Check all required modules exist
    required_modules = ["auth", "blogs", "candidates", "clients", "contact", "upload"]
    
    print("\nChecking module structure:")
    all_modules_valid = True
    
    for module in required_modules:
        module_path = api_path / module
        init_file = module_path / "__init__.py"
        router_file = module_path / "router.py"
        
        module_valid = True
        
        if not module_path.exists():
            print(f"  ✗ Module directory missing: {module}")
            module_valid = False
        else:
            if not init_file.exists():
                print(f"  ✗ __init__.py missing in: {module}")
                module_valid = False
            
            if not router_file.exists():
                print(f"  ✗ router.py missing in: {module}")
                module_valid = False
            
            if module_valid:
                print(f"  ✓ {module}: Complete")
        
        all_modules_valid = all_modules_valid and module_valid
    
    return all_modules_valid


def test_imports():
    """Test that all modules can be imported"""
    print("\nTesting module imports:")
    
    try:
        from app.api.auth import router as auth_router
        print("  ✓ auth module imports successfully")
    except ImportError as e:
        print(f"  ✗ auth import failed: {e}")
        return False
    
    try:
        from app.api.blogs import router as blogs_router
        print("  ✓ blogs module imports successfully")
    except ImportError as e:
        print(f"  ✗ blogs import failed: {e}")
        return False
    
    try:
        from app.api.candidates import router as candidates_router
        print("  ✓ candidates module imports successfully")
    except ImportError as e:
        print(f"  ✗ candidates import failed: {e}")
        return False
    
    try:
        from app.api.clients import router as clients_router
        print("  ✓ clients module imports successfully")
    except ImportError as e:
        print(f"  ✗ clients import failed: {e}")
        return False
    
    try:
        from app.api.contact import router as contact_router
        print("  ✓ contact module imports successfully")
    except ImportError as e:
        print(f"  ✗ contact import failed: {e}")
        return False
    
    try:
        from app.api.upload import router as upload_router
        print("  ✓ upload module imports successfully")
    except ImportError as e:
        print(f"  ✗ upload import failed: {e}")
        return False
    
    return True


def test_router_properties():
    """Test that routers have correct properties"""
    print("\nTesting router properties:")
    
    from app.api.candidates import router as candidates_router
    
    # Check candidate router has endpoints
    endpoints = list(candidates_router.routes)
    
    if len(endpoints) > 0:
        print(f"  ✓ Candidate router has {len(endpoints)} endpoints")
        
        # Check some key endpoints exist
        endpoint_paths = [route.path for route in endpoints]
        required_paths = ["/candidates/", "/candidates/{candidate_id}"]
        
        for path in required_paths:
            if any(path in ep for ep in endpoint_paths):
                print(f"  ✓ Required endpoint pattern found: {path}")
            else:
                print(f"  ✗ Required endpoint pattern missing: {path}")
                return False
    else:
        print("  ✗ Candidate router has no endpoints")
        return False
    
    return True


def test_main_imports():
    """Test that main.py can import all modules"""
    print("\nTesting main.py imports:")
    
    try:
        # Simulate what main.py does
        from app.api import candidates, clients, blogs, auth, upload, contact
        print("  ✓ All modules import successfully in main.py pattern")
        
        # Check routers exist
        assert hasattr(candidates, 'router')
        assert hasattr(clients, 'router')
        assert hasattr(blogs, 'router')
        assert hasattr(auth, 'router')
        assert hasattr(upload, 'router')
        assert hasattr(contact, 'router')
        print("  ✓ All modules have 'router' attribute")
        
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False
    except AssertionError as e:
        print(f"  ✗ Missing router attribute: {e}")
        return False
    
    return True


def main():
    """Run all architecture tests"""
    print("=" * 60)
    print("Testing API Architecture Consistency")
    print("=" * 60)
    
    tests = [
        ("API Structure", test_api_structure),
        ("Module Imports", test_imports),
        ("Router Properties", test_router_properties),
        ("Main Imports", test_main_imports)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Architecture Test Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n✅ API Architecture is consistent and well-structured!")
        print("\nArchitecture Summary:")
        print("1. ✅ All 6 API modules have consistent structure")
        print("2. ✅ Each module has __init__.py and router.py")
        print("3. ✅ All modules import correctly")
        print("4. ✅ Candidate router has comprehensive endpoints")
        print("5. ✅ Main.py can import all modules correctly")
        print("\nThe architecture follows the modular API pattern:")
        print("  app/api/")
        print("  ├── auth/          # Authentication")
        print("  ├── blogs/         # Blog management")
        print("  ├── candidates/    # Candidate registration (COMPLETE)")
        print("  ├── clients/       # Client management")
        print("  ├── contact/       # Contact enquiries")
        print("  └── upload/        # File upload (COMPLETE)")
    else:
        print("\n⚠️  Architecture needs improvement.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)