def is_eligible_for_loan(income: int, age: int, employment_status: str) -> bool:
    return (income >= 50000) and (age >= 21) and (employment_status == 'employed')
