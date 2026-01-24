import random

def generate_questions(grade: int, num: int = 30):
    questions = []
    
    for _ in range(num):
        a, b, op, ans = 0, 0, "", 0
        options = []
        
        # Grade 1-4: Basic Arithmetic
        if grade <= 4:
            limit = 10 * grade  # Grade 1 -> 10, Grade 4 -> 40
            if grade == 1:
                op = random.choice(["+", "-"])
                a = random.randint(1, 20)
                b = random.randint(1, 20)
            elif grade == 2:
                op = random.choice(["+", "-"])
                a = random.randint(10, 100)
                b = random.randint(1, 50)
            elif grade == 3:
                op = random.choice(["*", "/"])
                if op == "*":
                    a = random.randint(2, 10)
                    b = random.randint(2, 10)
                else:
                    b = random.randint(2, 10)
                    answer = random.randint(2, 10)
                    a = b * answer
            else: # Grade 4
                op = random.choice(["+", "-", "*", "/"])
                a = random.randint(10, 100)
                b = random.randint(2, 20)

        # Grade 5-8: Intermediate
        elif grade <= 8:
            op = random.choice(["+", "-", "*", "/"])
            limit = 100 * (grade - 3)
            a = random.randint(10, limit)
            b = random.randint(5, 50)
            
        # Grade 9-11: Advanced (Simplified for text bot)
        else:
             op = random.choice(["+", "-", "*", "/"])
             a = random.randint(50, 500)
             b = random.randint(10, 100)

        # Calculate Answer
        if op == "+":
            ans = a + b
        elif op == "-":
            ans = a - b
            # Avoid negative for lower grades if desired, but let's keep it simple
        elif op == "*":
            ans = a * b
        elif op == "/":
            # Ensure divisibility
            if grade >= 3:
                 # Re-generate valid division for simplicity or round
                 ans = a // b
                 a = ans * b # adjust a to be divisible
            else:
                 ans = a // b

        # Generate Options
        wrong1 = ans + random.randint(1, 5)
        wrong2 = ans - random.randint(1, 5)
        wrong3 = ans + random.randint(6, 10)
        
        # Ensure unique options
        opts = {ans, wrong1, wrong2, wrong3}
        while len(opts) < 3:
            opts.add(ans + random.randint(10, 20))
            
        options = list(opts)
        # Limit to 3 options for UI
        options = options[:3] 
        random.shuffle(options)

        # Format Question
        question_text = f"{a} {op} {b} = ?"
        
        questions.append({
            "q": question_text,
            "options": [str(o) for o in options],
            "answer": options.index(ans) # correct index
        })
        
    return questions
