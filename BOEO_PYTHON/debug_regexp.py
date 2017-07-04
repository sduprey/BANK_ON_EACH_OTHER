import re
import sys

def re_replace_or_die(string, varname, value):
    old_string = string
    new_string = re.sub(
        r"(uint constant *{} *=).*;".format(varname),
        r"\1 {};".format(value),
        string
    )
    if old_string == new_string:
        print(
            "ERROR: Could not match RE for '{}' during DAO's source "
            "code editing for the tests.".format(varname)
        )
        sys.exit(1)
    return new_string


if __name__ == "__main__":
#    re_replace_or_die(string, varname, value)
    ins = "uint constant minProposalDebatePeriod = 2 weeks;"
    print(ins)
    out = re_replace_or_die(ins, "minProposalDebatePeriod", "1")
    print(out)

    ins = "if (!allowedRecipients[_recipient]"+"| | _debatingPeriod < minProposalDebatePeriod"+"| | _debatingPeriod > 8 weeks"+"| | msg.value < proposalDeposit"+"| | msg.sender == address(this) // to prevent a 51 % attacker to convert the ether into deposit"+")"
    print(ins)
    out = re_replace_or_die(ins,"minProposalDebatePeriod", "1")
    print(out)


