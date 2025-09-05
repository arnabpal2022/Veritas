from app.workflow import create_workflow

workflow = create_workflow()

final_state = workflow.invoke({
    "articles": None,
    "summaries": None,
    "report": None
})
    
# Display results
print("\nDaily News Reports by Veritas\n")
print(final_state['report'])