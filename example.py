import torch
import re
from tools.extract_raw_matrix_str import extract_assignment_and_matrix
from tools.index_converter import convert_idx_for_var
from tools.matrix_wrapper_converter import matlab_matrix_to_python
from tools.variable_extractor import extract_matlab_variable_names

# convert matlab matrix to torch.tensor

def matlab_to_tensor(str):

    # get varname and raw matrix
    varname, mat = extract_assignment_and_matrix(str)

    # get rid of whitespace
    mat = ''.join(mat.split())

    # change .^ to **
    mat = mat.replace(".^", "**")

    # change .* to *
    mat = mat.replace(".*", "*")

    # add torch. to sin and cos, tan, cot
    mat = mat.replace("sin", "torch.sin")
    mat = mat.replace("cos", "torch.cos")
    mat = mat.replace("tan", "torch.tan")
    mat = mat.replace("cot", "torch.cot")

    # change x(i) to x[i-1] for all vars
    variables = extract_matlab_variable_names(mat)
    for v in variables:
        mat = convert_idx_for_var(mat, v)

    # change matlab matrix to python matrix
    mat = matlab_matrix_to_python(mat)

    out = "torch.tensor(" + mat + ")"

    return out

if __name__ == '__main__':
    test = "M=[2.*I1z+2.*I2z+Ipz+l1.^2.*(Mp+(3/2).*Ms+2.*Mt)+(1/2).*  l2.^2.*(2.*Mp+4.*Ms+3.*Mt)+l1.*l2.*(2.*(Mp+Ms)+3.*Mt).*cos(  x(2))+(-1).*l2.^2.*(2.*Ms+Mt).*cos(x(3))+(-1).*l1.*(l2.*(2.*  Ms+Mt).*cos(x(2)+x(3))+l2.*Ms.*((-1).*cos(x(4))+cos(x(3)+x(  4)))+l1.*Ms.*cos(x(2)+x(3)+x(4))),I1z+I2z+Ipz+(1/4).*(  l1.^2.*Ms+l2.^2.*(8.*Ms+5.*Mt))+l1.*l2.*(Ms+Mt).*cos(x(2))+(  -1/2).*l1.^2.*Ms.*cos(x(2)+x(3)+x(4))+(-1/4).*l2.*(l2.*(4.*  Mp+Mt).*cos(2.*(x(1)+x(2)))+2.*l1.*(2.*Mp+Mt).*cos(2.*x(1)+  x(2))+2.*(2.*Ms+Mt).*(2.*l2.*cos(x(3))+l1.*cos(x(2)+x(3)))+(  -8).*l1.*Ms.*cos(x(4)).*sin((1/2).*x(3)).^2+(-4).*l1.*Ms.*  sin(x(3)).*sin(x(4))),(1/4).*(4.*I1z+4.*I2z+l1.^2.*Ms+  l2.^2.*(4.*Ms+Mt)+(-2).*l2.^2.*(2.*Ms+Mt).*cos(x(3))+(-2).*  l1.*(l2.*(2.*Ms+Mt).*cos(x(2)+x(3))+l2.*Ms.*((-2).*cos(x(4))  +cos(x(3)+x(4)))+l1.*Ms.*cos(x(2)+x(3)+x(4)))),I1z+(1/4).*  l1.^2.*Ms+(-1/2).*l1.*Ms.*((-1).*l2.*cos(x(4))+l2.*cos(x(3)+  x(4))+l1.*cos(x(2)+x(3)+x(4)));I1z+I2z+Ipz+(1/4).*(l1.^2.*  Ms+l2.^2.*(8.*Ms+5.*Mt))+l1.*l2.*(Ms+Mt).*cos(x(2))+(-1/2).*  l1.^2.*Ms.*cos(x(2)+x(3)+x(4))+(-1/4).*l2.*(l2.*(4.*Mp+Mt).*  cos(2.*(x(1)+x(2)))+2.*l1.*(2.*Mp+Mt).*cos(2.*x(1)+x(2))+2.*  (2.*Ms+Mt).*(2.*l2.*cos(x(3))+l1.*cos(x(2)+x(3)))+(-8).*l1.*  Ms.*cos(x(4)).*sin((1/2).*x(3)).^2+(-4).*l1.*Ms.*sin(x(3)).*  sin(x(4))),I1z+I2z+Ipz+(1/4).*(l1.^2.*Ms+l2.^2.*(4.*Mp+8.*  Ms+6.*Mt))+(-1).*l2.^2.*(2.*Ms+Mt).*cos(x(3))+l1.*l2.*Ms.*(  cos(x(4))+(-1).*cos(x(3)+x(4))),(1/4).*(4.*I1z+4.*I2z+  l1.^2.*Ms+l2.^2.*(4.*Ms+Mt)+(-2).*l2.*(l2.*(2.*Ms+Mt).*cos(  x(3))+l1.*Ms.*((-2).*cos(x(4))+cos(x(3)+x(4))))),I1z+(1/4).*  l1.^2.*Ms+(1/2).*l1.*l2.*Ms.*(cos(x(4))+(-1).*cos(x(3)+x(4))  );(1/4).*(4.*I1z+4.*I2z+l1.^2.*Ms+l2.^2.*(4.*Ms+Mt)+(-2).*  l2.^2.*(2.*Ms+Mt).*cos(x(3))+(-2).*l1.*(l2.*(2.*Ms+Mt).*cos(  x(2)+x(3))+l2.*Ms.*((-2).*cos(x(4))+cos(x(3)+x(4)))+l1.*Ms.*  cos(x(2)+x(3)+x(4)))),(1/4).*(4.*I1z+4.*I2z+l1.^2.*Ms+  l2.^2.*(4.*Ms+Mt)+(-2).*l2.*(l2.*(2.*Ms+Mt).*cos(x(3))+l1.*  Ms.*((-2).*cos(x(4))+cos(x(3)+x(4))))),I1z+I2z+(1/4).*(  l1.^2.*Ms+l2.^2.*(4.*Ms+Mt))+l1.*l2.*Ms.*cos(x(4)),I1z+(1/4)  .*l1.^2.*Ms+(1/2).*l1.*l2.*Ms.*cos(x(4));I1z+(1/4).*l1.^2.*  Ms+(-1/2).*l1.*Ms.*((-1).*l2.*cos(x(4))+l2.*cos(x(3)+x(4))+  l1.*cos(x(2)+x(3)+x(4))),I1z+(1/4).*l1.^2.*Ms+(1/2).*l1.*  l2.*Ms.*(cos(x(4))+(-1).*cos(x(3)+x(4))),I1z+(1/4).*l1.^2.*  Ms+(1/2).*l1.*l2.*Ms.*cos(x(4)),I1z+(1/4).*l1.^2.*Ms]"
    variables = extract_matlab_variable_names(test)
    out = matlab_to_tensor(test)
    print(f"Variables inside the matrix include: {variables}")
    print(out)