from database import create_table
from login import LoginWindow

create_table()

app = LoginWindow()
app.root.mainloop()