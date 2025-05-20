

# import logging

# try:
#     import watchtower
# except ImportError:
#     watchtower = None

# class SafeWatchtowerHandler(logging.Handler):
#     def __init__(self, *args, **kwargs):
#         super().__init__()
#         if watchtower:
#             try:
#                 self.wt_handler = watchtower.CloudWatchLogHandler(
#                     log_group=kwargs.get("log_group", "MyLog"),
#                     stream_name=kwargs.get("stream_name", "MyStream"),
#                     use_queues=False
#                 )
#             except Exception as e:
#                 self.wt_handler = None
#                 print(f"Watchtower setup failed: {e}")
#         else:
#             self.wt_handler = None

#     def emit(self, record):
#         if self.wt_handler:
#             self.wt_handler.emit(record)




# import logging

# try:
#     import watchtower
# except ImportError:
#     watchtower = None

# class SafeWatchtowerHandler(logging.Handler):
#     def __init__(self, *args, **kwargs):
#         super().__init__()

#         # Check if Watchtower is installed
#         if watchtower:
#             try:
#                 # Try initializing the CloudWatchLogHandler
#                 self.wt_handler = watchtower.CloudWatchLogHandler(
#                     log_group=kwargs.get("log_group", "MyLog"),
#                     stream_name=kwargs.get("stream_name", "MyStream"),
#                     use_queues=False
#                 )
#                 # Log successful initialization
#                 logging.info(f"Watchtower handler initialized with log group '{kwargs.get('log_group', 'MyLog')}' and stream '{kwargs.get('stream_name', 'MyStream')}'")
#                   # ✅ Add this line right here
#                 print("Watchtower initialized:", bool(self.wt_handler))
            
#             except Exception as e:
#                 # If there is an issue with initialization, log the error
#                 self.wt_handler = None
#                 logging.error(f"Watchtower setup failed: {e}")
#         else:
#             # Log warning if watchtower is not installed
#             self.wt_handler = None
#             logging.warning("Watchtower module is not installed. Logs will not be sent to CloudWatch.")

#     def emit(self, record):
#         if self.wt_handler:
#             try:
#                 # Attempt to emit the log record to CloudWatch
#                 self.wt_handler.emit(record)
#             except Exception as e:
#                 # If emitting the log to CloudWatch fails, log the error
#                 logging.error(f"Failed to emit log to CloudWatch: {e}")
#         else:
#             # If the handler is not initialized, log the issue
#             logging.warning("Watchtower handler is not initialized. Logs will not be sent to CloudWatch.")








# import logging
# import boto3

# try:
#     import watchtower
# except ImportError:
#     watchtower = None

# class SafeWatchtowerHandler(logging.Handler):
#     def __init__(self, *args, **kwargs):
#         super().__init__()

#         # Hardcoded region
#         region = "us-west-2"  # Replace with your desired AWS region

#         # Check if Watchtower is installed
#         if watchtower:
#             try:
#                 # Create a boto3 session with the hardcoded region
#                 session = boto3.Session(region_name=region)

#                 # Try initializing the CloudWatchLogHandler
#                 self.wt_handler = watchtower.CloudWatchLogHandler(
#                     boto3_session=session,
#                     log_group=kwargs.get("log_group", "MyLog"),
#                     stream_name=kwargs.get("stream_name", "MyStream"),
#                     use_queuenes=False
#                 )
#                 # Log successful initialization
#                 logging.info(f"Watchtower handler initialized with log group '{kwargs.get('log_group', 'MyLog')}' and stream '{kwargs.get('stream_name', 'MyStream')}' in region '{region}'")
#                 print("Watchtower initialized:", bool(self.wt_handler))
            
#             except Exception as e:
#                 # If there is an issue with initialization, log the error
#                 self.wt_handler = None
#                 logging.error(f"Watchtower setup failed: {e}")
#         else:
#             # Log warning if watchtower is not installed
#             self.wt_handler = None
#             logging.warning("Watchtower module is not installed. Logs will not be sent to CloudWatch.")

#     def emit(self, record):
#         if self.wt_handler:
#             try:
#                 # Attempt to emit the log record to CloudWatch
#                 self.wt_handler.emit(record)
#             except Exception as e:
#                 # If emitting the log to CloudWatch fails, log the error
#                 logging.error(f"Failed to emit log to CloudWatch: {e}")
#         else:
#             # If the handler is not initialized, log the issue
#             logging.warning("Watchtower handler is not initialized. Logs will not be sent to CloudWatch.")





# # core/logging_handlers.py

# import logging
# import boto3

# try:
#     import watchtower
# except ImportError:
#     watchtower = None

# class SafeWatchtowerHandler(logging.Handler):
#     def __init__(self, *args, **kwargs):
#         logging.Handler.__init__(self)  # safer than super()
        
#         region = "us-west-2"
#         self.setLevel(kwargs.get("level", logging.INFO))

#         if watchtower:
#             try:
#                 session = boto3.Session(region_name=region)
#                 self.wt_handler = watchtower.CloudWatchLogHandler(
#                     boto3_session=session,
#                     log_group=kwargs.get("log_group", "MyLog"),
#                     stream_name=kwargs.get("stream_name", "MyStream"),
#                     use_queues=False  # ✅ fixed typo here
#                 )
#                 self.wt_handler.setLevel(self.level)

#                 logging.info(f"✅ Watchtower initialized for '{kwargs.get('log_group')}' in region '{region}'")

#             except Exception as e:
#                 self.wt_handler = None
#                 logging.error(f"❌ Watchtower setup failed: {e}")

#         else:
#             self.wt_handler = None
#             logging.warning("⚠️ Watchtower is not installed.")

#     def emit(self, record):
#         if self.wt_handler:
#             try:
#                 self.wt_handler.emit(record)
#             except Exception:
#                 self.handleError(record)  # better than logging again
#         else:
#             pass  # no-op if handler not initialized




# # # core/logging_handlers.py
# import logging
# import boto3

# try:
#     import watchtower
# except ImportError:
#     watchtower = None

# class SafeWatchtowerHandler(logging.Handler):
#     def __init__(self, *args, **kwargs):
#         logging.Handler.__init__(self)

#         region = kwargs.get("region_name", "us-west-2")
#         self.setLevel(kwargs.get("level", logging.INFO))

#         if watchtower:
#             try:
#                 session = boto3.Session(region_name=region)
#                 self.wt_handler = watchtower.CloudWatchLogHandler(
#                     boto3_session=session,
#                     log_group=kwargs.get("log_group", "MyLog"),
#                     stream_name=kwargs.get("stream_name", "MyStream"),
#                     use_queues=False,
#                     create_log_group=True,
#                     create_log_stream=True,
#                 )
#                 self.wt_handler.setLevel(self.level)

#                 logging.info(f"✅ Watchtower initialized for '{kwargs.get('log_group')}' in region '{region}'")

#             except Exception as e:
#                 self.wt_handler = None
#                 logging.error(f"❌ Watchtower setup failed: {e}")

#         else:
#             self.wt_handler = None
#             logging.warning("⚠️ Watchtower is not installed.")

#     def emit(self, record):
#         if self.wt_handler:
#             try:
#                 self.wt_handler.emit(record)
#             except Exception:
#                 self.handleError(record)
