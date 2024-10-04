# Simulating manual arthmetic operations
#### Video Demo:  https://youtu.be/fWOWn5EfbFY
#### Description:

  #### Input
      Input is taken as a command value which can be either:
      '\help', '\history', '\steps' or a mathematical expression that is evaluated by the program.
      If correct, it is passed accordingly by operation (-, +, *, /) 
      to the function responsible for that type of calculation.

      After every new command, the command screen is cleared,
      so at a given time only one mathematical calculation is being expressed,
      preventing the user from being flooded by a mass of text that they must filter through themselves.
  #### Errors
      I decided to only raise a ValueError when something undesirable occurs.
      This is triggered by a try-except block in the main function, which provides a prompt about incorrect input.
      If an unrecognizable command is inputted three times in a row,
      the program recognizes that the user might be confused and provides additional information if the user types '\help'.
  #### Choice between output lenght
      By default, any given input only prints the final calculation answer. The user, by typing '\steps',
      has the ability to switch between printing only the default option
      and a full step-by-step logic behind every calculation done to get to the final output.
      Every step is separated by a block of three dots representing loading until the final output,
      with an interval of one step every 1.5 seconds.
  #### Recording user activity
      With every correct equation that the user inputs, it will be stored in a CSV file.
      When the user enters the history submenu,
      every operation done up until now is presented in descending list order.
      The user can type the index of the equation that will be calculated again or type '\history' again to quit this submenu.
  #### Saving data to PDF
      Inside the history submenu, the user has the ability to save calculations to a PDF file by typing \save index_number.
      This will generate a PDF file with the same name as the equation inside the program folder.
      A successful operation will prompt the user with the location of the saved file.
      Inside the history submenu, the user can also switch between step-by-step calculations,
      so the PDF file will either be one table short or multiple tables of content in order to get the answer.
  ####
      The user can quit the program by triggering an EOFError (on Windows systems only) by pressing CTRL+Z.
      This stops the program and deletes the entire history of operations done during the program's runtime.

  ### How calculations work explained, design choice
      There are four core functions: Addition, Subtraction, Multiplication, and Division,
      that each do their own calculations and always yield output to a generator that prints data. 
      
      They work by reading lists from right to left and performing corresponding operations on those lists, as we would do with pen and paper.
      For example, the last element of the subtraction 407-315 is 5 and 6, giving the output 7-5=2 at the last index of the output list,
      then moving to the next index from the right, analyzing it from two lists.

      To give it a look close to handwritten calculations, every print is done using the tabulate library,
      as I believe it's the most similar approach to making it look like paper-written calculations.
      All of these prints, except for Division, are done in the print_output function,
      which selects the variation of tabulate content that fits the given type of operation.

      Division operation is the only one where 
      I decided to prompt the answer as users not understanding manual calculation of division might be confused about what the answer is.
      I have made it so that if a number has no decimal points it ends with the '=' character,
      and if it ends with a fraction like 4 while the divisor is, for example, 5,
      the program will prompt the user that the given calculation results in a fraction of 4/5.
      
      For multiplication, if choosing long steps i decided to indicate 
      which number is currently being multiplied by enclosing it in square brackets.
      
      Previously, I had done the final step of summing every multiplication output inside the Addition function,
      but because of adding generator yields, it no longer works,
      so I had to make a multi_addition function that is very similar to the Addition function,
      and a subtracting_division function similar to the Subtraction function.
      These changes by adding generator yields made the motion between steps more fluid
      as opposed to printing inside for loops of those functions and adding os.sleep.
      
      In the test_project file, I wanted to check my results to see if the printed tables were correct,
      but it seems pytest doesn't recognize it,
      so I at least tested those similar functions of addition and subtraction that show my program calculations are correct.
      
