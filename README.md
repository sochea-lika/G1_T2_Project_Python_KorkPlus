<h1 align="center">Kork Plus</h1>

1. Description: Kork Plus is application  has 2 role is Admin and User. Admin can mangae event and ticket. User can booking ticket event.    
2. Feature 
- [Admin](#Admin)
   - [Add Event](#add-event)
   - [Edit Event](#edit-evenn)
   - [View Event](#view-event)
   - [Delete Event](#delete-event)
   - [View ticket per event](#View-ticket)
   - [View Admin Accounts](#view-admin-acoount)
- [User](#user)
    - [Create Booking](#create-booking)
    - [Cancel Booking](#cancel-booking)
    - [View all Event](#view-all-events)
    - [View all Booking](#view-mybooking)
    - [View my cancel booking](#view-mycancelbookin)  

3. Library 

 - [OS Library](#os-library)
 - [Datetime Libaray](#datetime-library)
 - [Msvcrt libaray](#msvcrt-library)
 - [Sys library](#sys-library)

    3.1 Requirements
     - [Python 3.x or higher](#version-python)
     - [Window Operating System](#window)

4. Installation  
   
  - [go to terminal](#terminal) to downlode virtual environment
   ```
   python -m venv .venv
   if you use:
      1 Window/cmd: .venv\Scripts\activate
      2 git bash: source venv/Scripts/activate
      3 linux/Mac: source .venv/bin/activate
   And then install rich
   pip install matplotlib rich
   Note** virtual  environment libarary must install before rich libaray
   ```

5. Usage 

1.Open the terminal or cammand prompt

2.Navigate to the project folder

3.Run the program: python run.py

    ```
    Menu:
    1.Admin Panel
    2.User Panel
    3.Exit
    -> Click 1 (Admin)
       Admin:
       1.Register
       2.Sign in
       3.Forget Password
       4.Exit program
       -> Click 1 (Register)
         .Enter Username
         .Enter Email
         .Enter password :required strong password
         ✅ If successfull show Analyst Dashbord : Total Revenue, Top Seller and Cirtical Seat. Go to page Admin Dashboard
      -> Click 2 (Sign in)
         .Enter gmail
         .Verify password
         ✅ If successfull show Analyst Dashboard :Total Revenue, Top Seller and Cirtical Seat. 
         👉 Press Enter to go to Admin Dashboard
          1.Add New Event
          2.Edit Existing
          3.Browse Events
          4.Delete Event
          5.Sales Overview
          6.Cancel ticket
          7.Admin Account
          8.Analysis
          9.Lagout
          10.Shutdown System
         -> Click 1 (Add new event)
            . Enter Title
            . Enter Data: required Format(YYYY-MM-DD)
            . Enter Location
            . Enter Description
            . Enter Price
            . Enter Total Seats : required interger not float
         -> Click 2 (Edit event)
            . Enter ID event
            . If don't want to update just click key "Enter"
         -> Click 3 (View all events)
            . Program show all events with all info's events
            . Press Enter to back to Dashboard Admin
         -> Click 4 (Delete event)
            . Enter ID event
            . Program will ask you make sure want delete or not just write "y" for yes and 
            "n" for no
         -> Click 5 (Sale overview)
            . Show Event Title, Sales Progress(percent %), Sold, Remaining and Status
            . Press Enter to  back Admin Dashbord
         -> Click 6 (Cancel Ticket) : Analyst cancel Ticket
         -> Click 7 (Admin Account) 
            . show all accounts admin (No, username, Email and Role)
            . Press Enter to back Admin dashboard
         -> Click 8 (Analysis)
            1. View Daily Sales Trend :
               . Dialy can press Enter or Write word  Dialy
               . Weekly write word weekly
               . Monthly write word monthly    
            2. View Top and Lowest Performce
            3. Detail Revenur Breakdown 
            4. Back to Main Dashbord
         -> Click 9 (Logout) : Back to Admin Page
         -> Click 10 (Shut down system): close program
      
      -> Click 3 (Recover Password)
         . Enter gamil
         . Enter new password : requiredment strong password