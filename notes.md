# Notes

## 🧪 What are Unit Tests?

**Definition:** Unit tests are small, automated tests that check whether individual pieces of your code (functions, classes, methods) work correctly in isolation.

**Goal:** Catch bugs early by verifying that each “unit” of logic behaves as expected.

**Scope:** They don’t test the whole system end‑to‑end, just one function or module at a time.

**Frameworks:** In Python, the most common are `unittest` (built‑in) and `pytest` (popular, simpler syntax).

---

## Things to check

- [x] Paths following this pattern: `Path(__file__).resolve().parent.parent / "data"`
- [x] The annual retention value is the sum of the projected tax? Yes
- [ ] Introduce a validation to the maximum deductible value

## Future considerations

Link: https://www.jezl-auditores.com/index.php/tributario/115-proyeccion-de-gastos-personales-2025

- [ ] Check the number of months to applicate the division of the projected values (11?)
- [ ] Check the case where a new projection is introduced in the middle of the year
- [ ] Check the use of family members