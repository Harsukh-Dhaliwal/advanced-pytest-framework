from faker import Faker

fake = Faker()

class TestDataMutator:
    """Enterprise generation engine provisioning randomized parameter mutations for E2E form integrity."""
    
    @staticmethod
    def generate_user_profile() -> dict:
        """Returns a randomized user data profile mutation packet."""
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"automation_{first_name.lower()}_{fake.random_int(100, 999)}@example.ca",
            "postal_code": fake.postcode() if fake.postcode() else "L6P 0A1", # Local contextual fallback structure
            "notes": f"Automated structural testing entry triggered on {fake.date()}"
        }