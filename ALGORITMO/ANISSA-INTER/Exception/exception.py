#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

"""
\package exception
\brief This module manages all information related to exceptions.
"""

class GenException(Exception):
    """ 
    \brief Class that manages the generic exception.   
    """   
    def __init__(self, value):
        """
        \brief Initialize all the components of class GenException.
        \param self (exception::GenException).
        \param value Exception value.       
        \return No return.
        """
        ## Exception value
        self.value = value

    def __str__(self):
        """
        \brief Printable method.
        \param self (exception::GenException).
        \return (str) Error message.
        """
        return "Error " + str(self.value)
    
class ShowImageException(Exception):
    """ 
    \brief Class that manages the show image exception.   
    """ 
    def __init__(self, value):
        """
        \brief Initialize all the components of class ShowImageException.
        \param self (exception::GenException).
        \param value Exception value.       
        \return No return.
        """
        ## Exception value
        self.value = value

    def __str__(self):
        """
        \brief Printable method.
        \param self (exception::GenException).
        \return (str) Error message.
        """
        return "Error " + str(self.value)
    
class ShowThumbnailException(Exception):
    """ 
    \brief Class that manages the show thumbnail exception.   
    """ 
    def __init__(self, value):
        """
        \brief Initialize all the components of class ShowImageException
        \param self (exception::GenException).
        \param value Exception value.       
        \return No return.
        """
        ## Exception value
        self.value = value

    def __str__(self):
        """
        \brief Printable method.
        \param self (exception::GenException).
        \return (str) Error message.
        """
        return "Error " + str(self.value)
