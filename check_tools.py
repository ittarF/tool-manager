"""
Script to check what tools are available in the database
"""
from app.database import SessionLocal
from app.models import Tool

def check_tools():
    """List all tools in the database"""
    db = SessionLocal()
    try:
        tools = db.query(Tool).all()
        print(f"Found {len(tools)} tools in database:")
        for i, tool in enumerate(tools):
            print(f"{i+1}. {tool.name}: {tool.description} (Native: {tool.is_native})")
            if tool.is_native:
                print(f"   Function path: {tool.function_path}")
    finally:
        db.close()

if __name__ == "__main__":
    check_tools() 