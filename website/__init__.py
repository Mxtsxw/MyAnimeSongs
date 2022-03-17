try:
  from .app import app
except:
  import traceback
  traceback.print_last()
  
import website.views
import website.commands
import website.api