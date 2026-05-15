from enum import StrEnum


class NutshellEnum(StrEnum):
  pass


class UserRole(NutshellEnum):
  admin = "Admin"
  user = "User"
