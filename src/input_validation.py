def input_int_with_limits(message: str, lower_bound: int, upper_bound: int) -> int:
    option = 0
    while(True):
        try:
            option = int(input(message))
            if (lower_bound and upper_bound):
                assert(option > lower_bound and option < upper_bound)
            break
        except ValueError as e:
            print("Please enter a positive integer.")
        except AssertionError as e:
            print("Please enter a number between {0} and {1}.".format(lower_bound+1, upper_bound-1))
    return(option)
