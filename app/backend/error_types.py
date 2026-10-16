from enum import Enum


class ErrorType(str, Enum):
    SyntaxError = 'SyntaxError'
    IndentationError = 'IndentationError'
    TypeError = 'TypeError'
    ImportError = 'ImportError'
    NameError = 'NameError'
    LogicError = 'LogicError'
    InfiniteLoop = 'InfiniteLoop'
    BoundaryError = 'BoundaryError'
    NullSafety = 'NullSafety'
    DataStructureMisuse = 'DataStructureMisuse'
    Efficiency = 'Efficiency'
    RedundantCode = 'RedundantCode'
    NamingConvention = 'NamingConvention'
    Security = 'Security'
    Documentation = 'Documentation'
    Other = 'Other'
