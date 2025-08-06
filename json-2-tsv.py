import json

def convert_json_to_tsv(json_file_path, tsv_file_path, user_tags):
    """
    Converts a JSON file of quiz questions to a TSV file with a specific format.
    Handles cases where 'Answer' may be an int or string.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in '{json_file_path}'.")
        return

    # TSV Header
    tsv_header = [
        "#separator:tab",
        "#html:true",
        "#tags column:10"
    ]

    tsv_lines = []
    for i, question in enumerate(questions_data, 1):
        sl = "-"  # Always hyphen now
        question_text = str(question.get("Question", "")).replace('\n', '<br>')
        op1 = question.get("OP1", "")
        op2 = question.get("OP2", "")
        op3 = question.get("OP3", "")
        op4 = question.get("OP4", "")

        # Handle 'Answer' safely, whether it's int or str
        raw_answer = question.get("Answer", "")
        if raw_answer is None:
            answer = ""
        else:
            answer = str(raw_answer).strip()

        extra = ""  # Blank as per latest rule
        video = ""  # Blank as per latest rule
        tags = user_tags.strip()

        tsv_row = [
            sl, question_text, op1, op2, op3, op4,
            answer, extra, video, tags
        ]

        # Ensure all elements are strings
        tsv_lines.append('\t'.join(map(str, tsv_row)))

    # Write to file
    try:
        with open(tsv_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(tsv_header) + '\n')
            f.write('\n'.join(tsv_lines) + '\n')
        print(f"✅ Successfully converted '{json_file_path}' → '{tsv_file_path}'")
    except IOError as e:
        print(f"❌ File write error: {e}")

# Run the script
if __name__ == "__main__":
    user_tags = input("Please enter the tags (e.g., CGL::Mains::004 MATH): ")
    convert_json_to_tsv('questions.json', 'questions.txt', user_tags)
