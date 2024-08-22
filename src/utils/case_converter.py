class CaseConverter:
  @staticmethod
  def camel_case_to_snake_case(string: str) -> str:
    """
    camel_case_to_snake_case("SomeSDK") -> 'some_sdk'\n
    camel_case_to_snake_case("RServoDrive") -> 'r_servo_drive'\n
    camel_case_to_snake_case("SDKDemo") -> 'sdk_demo'\n
    """
    chars = []
    for current_index, char in enumerate(string):
      if current_index and char.isupper():
        next_index = current_index + 1
        flag = next_index >= len(string) or string[next_index].isupper()
        prev_char = string[current_index - 1]
        if prev_char.isupper() and flag:
          pass
        else:
          chars.append("_")

      chars.append(char.lower())

    return "".join(chars)
