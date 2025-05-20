# import logging
# from django.http import HttpResponse


# logger = logging.getLogger(__name__)

# def real_view(request):
#     logger.info("Real view accessed")
#     logger.warning("Something might be off...")
#     logger.error("Something went wrong!")
#     return HttpResponse("Real logging in action!")

# def test_logging_view(request):
#     logger.info("Test log triggered from test_logging_view")
#     return HttpResponse("Logging test successful")



import logging
from django.shortcuts import render
from django.http import HttpResponse

# Initialize the logger globally
logger = logging.getLogger(__name__)

def home(request):
    logger.info("Home page was visited.")
    return render(request, "home.html")

def submit_form(request):
    if request.method == "POST":
        logger.info("Form submitted successfully.")
        name = request.POST.get("name")
        
        # Check if the 'name' field is empty
        if not name:
            logger.error("Name was not provided in the form.")
            return HttpResponse("Error: Name is required", status=400)
        
        logger.info(f"Received name: {name}")
        return HttpResponse(f"Hello, {name}!")
    
    logger.warning("Received an invalid request method.")
    return HttpResponse("Invalid request", status=405)

def crash(request):
    # Log an error and a warning before crashing
    logger.error("🔥 Error triggered from Django route")
    logger.warning("Crash endpoint hit — about to divide by zero!")

    try:
        # Purposefully cause a crash (ZeroDivisionError)
        result = 1 / 0
    except ZeroDivisionError as e:
        # Log the exception with the full stack trace
        logger.exception("An exception occurred: ZeroDivisionError")
        return HttpResponse("An error occurred. Please try again later.", status=500)

    # If somehow the division doesn't crash (which it will), return this:
    return HttpResponse("Crashed.")
