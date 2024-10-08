# player_utils.py

def get_player_name(initials):
    player_mapping = {
        'JB': 'Jon BAKER',
        'AB': 'Alex BAKER',
        'GW': 'Gregg WILLIAMS',
        'DM': 'David MULLIN',
        'SN': 'Stuart NEUMANN',
        'JP': 'John PATTERSON',
        'HM': 'Henry MELLER'
    }
    
    return player_mapping.get(initials, f"Unknown Player ({initials})")

# Test the function if this script is run directly
if __name__ == "__main__":
    # Test cases
    test_cases = ['JB', 'AB', 'GW', 'DM', 'SN', 'JP', 'HM', 'XX']
    
    print("Testing get_player_name function:")
    for initials in test_cases:
        result = get_player_name(initials)
        print(f"Initials: {initials} -> Name: {result}")

    # You can add more specific tests here if needed
    assert get_player_name('JB') == 'Jon BAKER', "Test failed for 'JB'"
    assert get_player_name('XX') == 'Unknown Player (XX)', "Test failed for unknown player"

    print("All tests passed!")