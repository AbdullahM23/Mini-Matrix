class SquareMatrix:
    #Constructor
    def __init__(self, size, contents = []):
        if(type(size) != int):
            raise TypeError("SquareMatrix-Constructor: Invalid arguments used. Size must be of int type.")
        if(type(contents) != list):
            raise TypeError("SquareMatrix-Constructor: Invalid arguments used. Contents must be of list type.")

        self.size = size
        self.content = contents.copy()

        if(self.content != []):
            if(len(self.content) != self.size):
                raise ValueError("SquareMatrix-Constructor: Invalid arguments used. Contents array length and size conflict.")
            if(len(self.content) == 1):
                if(type(self.content[0]) == list and len(self.content[0]) != 1):
                    raise ValueError("SquareMatrix-Constructor: Invalid arguments used. Contents array lengths are not fit for a square matrix.")
                if(type(self.content[0]) != list):
                    self.content[0] = [self.content[0]]
            else:
                for i in self.content:
                    if(type(i) != list or len(i) != len(self.content)):
                        raise ValueError("SquareMatrix-Constructor: Invalid arguments used. Contents array lengths are not fit for a square matrix.")
        else:
            for i in range(self.size):
                self.content.append([])
                for j in range(self.size):
                    self.content[i].append(0)
    #I/O methods
    def GetAsString(self):
        string = ""
        for i in range(self.size):
            for j in range(self.size):
                string += str(self.content[i][j]) + " "
            string = string.rstrip() + "\n"
        return string.strip()
    def Print(self):
        print(self.GetAsString())
    def GetContent(self):
        theContent = []
        for i in range(self.size):
            theContent.append(list(self.content[i]))
        return theContent
    #Important Matrices
    @staticmethod
    def Identity(size):
        I = SquareMatrix(size)
        for i in range(I.size):
            I.SetElementByIndex(i+1, i+1, 1)
        return I
    @staticmethod
    def OnesMatrix(size):
        A = SquareMatrix(size)
        for i in range(A.size):
            for j in range(A.size):
                A.SetElementByIndex(i+1, j+1, 1)
        return A

    #"Self" methods
    def GetElementByIndex(self, row, col):
        return self.content[row-1][col-1]
    def SetElementByIndex(self, row, col, value):
        self.content[row-1][col-1] = value
    def GetRowByIndex(self, index):
        return self.content[index-1]
    def SetRowByIndex(self, index, value):
        if(len(value) != self.size):
            print("Invalid row size used, a row of size " + str(self.size) + " is needed.")
            return False
        self.content[index-1] = value
        return True
    def GetColByIndex(self, index):
        col = []
        for i in range(self.size):
            col.append(self.content[i][index-1])
        return col
    def SetColByIndex(self, index, value):
        if(len(value) != self.size):
            print("Invalid column size used, a column of size " + str(self.size) + " is needed.")
            return False
        for i in range(self.size):
            self.content[i][index-1] = value[i]
        return True
    def Scale(self, scale): #Scales a matrix by scale when called through that matrix
        for i in range(self.size):
            for j in range(self.size):
                self.content[i][j] *= scale
    def ScaleRow(self, index, scale): #Same as Scale but for 1 row
        for i in range(self.size):
            self.content[index-1][i] *= scale
    def ScaleCol(self, index, scale): #Same as Scale but for 1 column
        for i in range(self.size):
            self.content[i][index-1] *= scale
    def Transpose(self):
        A = SquareMatrix(self.size)
        for i in range(self.size):
            A.SetColByIndex(i + 1, self.GetRowByIndex(i + 1))
        self.content = A.GetContent()
    def Inverse(self):
        det = SquareMatrix.Det(self)
        if(det == 0):
            print("Matrix is uninvertible.")
            return
        self.content = SquareMatrix.Adjugate(self).GetContent()
        self.Scale(1 / det)

    #"Non-self"/"Abstract" methods
    @staticmethod
    def Equal(A, B):
        return A.GetContent() == B.GetContent()
    @staticmethod
    def Add(A, B): #A+B
        if(A.size != B.size):
            print("Invalid addition attempt, cannot add a matrix of size " + str(A.size) + " to a matrix of size " + str(B.size))
            return None
        C = SquareMatrix(A.size)
        for i in range(C.size):
            for j in range(C.size):
                C.SetElementByIndex(i+1, j+1, A.GetElementByIndex(i+1, j+1) + B.GetElementByIndex(i+1, j+1))
        return C
    @staticmethod
    def Sub(A, B): #A-B
        if(A.size != B.size):
            print("Invalid subtraction attempt, cannot subtract a matrix of size " + str(B.size) + " from a matrix of size " + str(A.size))
            return None
        C = SquareMatrix(A.size)
        for i in range(C.size):
            for j in range(C.size):
                C.SetElementByIndex(i+1, j+1, A.GetElementByIndex(i+1, j+1) - B.GetElementByIndex(i+1, j+1))
        return C
    @staticmethod
    def Mul(A, B): #AB
        if(A.size != B.size):
            print("Invalid multiplication attempt, cannot multiply a matrix of size " + str(A.size) + " and a matrix of size " + str(B.size))
            return None
        C = SquareMatrix(A.size)
        for i in range(C.size):
            for j in range(C.size):
                temp = 0
                for k in range(C.size):
                    temp += A.GetElementByIndex(i+1, k+1) * B.GetElementByIndex(k+1, j+1)
                C.SetElementByIndex(i+1, j+1, temp)
        return C
    @staticmethod
    def Scaled(matrix, scale): #Takes a matrix's values as A and returns a new matrix that is A scaled by scale
        A = SquareMatrix(matrix.size)
        for i in range(A.size):
            for j in range(A.size):
                A.SetElementByIndex(i+1, j+1, matrix.GetElementByIndex(i+1, j+1) * scale)
        return A
    @staticmethod
    def ScaledRow(matrix, index, scale): #Same as Scaled but for 1 row
        A = SquareMatrix(matrix.size)
        for i in range(A.size):
            for j in range(A.size):
                A.SetElementByIndex(i+1, j+1, matrix.GetElementByIndex(i+1, j+1))
        A.ScaleRow(index, scale)
        return A
    @staticmethod
    def ScaledCol(matrix, index, scale): #Same as Scaled but for 1 column
        A = SquareMatrix(matrix.size)
        for i in range(A.size):
            for j in range(A.size):
                A.SetElementByIndex(i+1, j+1, matrix.GetElementByIndex(i+1, j+1))
        A.ScaleCol(index, scale)
        return A
    @staticmethod
    def Cofactor(row, col, matrix): #Returns the submatrix that is the cofactor of the element at (row, col) in matrix
        if(row > matrix.size or col > matrix.size):
            print("Invalid row or column choice for cofactor computation. Index greater than matrix size.")
            return None
        if(matrix.size == 0):
            print("Invalid matrix input. Matrix is empty (0x0 matrix).")
            return None
        output = SquareMatrix(matrix.size - 1)
        i2 = 1
        for i1 in range(matrix.size):
            if(i1 == row - 1):
                continue
            j2 = 1
            for j1 in range(matrix.size):
                if(j1 == col - 1):
                    continue
                output.SetElementByIndex(i2, j2, matrix.GetElementByIndex(i1 + 1, j1 + 1))
                j2 += 1
            i2 += 1
        return output
    @staticmethod
    def Adjugate(matrix):
        A = SquareMatrix(matrix.size)
        for i in range(A.size):
            for j in range(A.size):
                temp = SquareMatrix.Det(SquareMatrix.Cofactor(i+1, j+1, matrix))
                if((i+j) % 2 == 1):
                    temp *= -1
                A.SetElementByIndex(i+1, j+1, temp)
        A.Transpose()
        return A
    @staticmethod
    def Det(matrix):
        if(matrix.size == 1):
            return matrix.GetElementByIndex(1, 1)
        det = 0
        for i in range(matrix.size):
            increment = matrix.GetElementByIndex(1, i + 1) * SquareMatrix.Det(SquareMatrix.Cofactor(1, i+1, matrix))
            if(i % 2 == 1):
                increment *= -1
            det += increment
        return det
    @staticmethod
    def Trace(matrix):
        trace = 0
        for i in range(matrix.size):
            trace += matrix.GetElementByIndex(i + 1, i + 1)
        return trace
    @staticmethod
    def Transposed(matrix):
        A = SquareMatrix(matrix.size)
        for i in range(matrix.size):
            A.SetColByIndex(i + 1, matrix.GetRowByIndex(i + 1))
        return A
    @staticmethod
    def Inversed(matrix):
        det = SquareMatrix.Det(matrix)
        if(det == 0):
            print("Matrix is uninvertible.")
            return None
        A = SquareMatrix.Adjugate(matrix)
        A.Scale(1 / det)
        return A
    @staticmethod
    def Commutator(A, B): #Gives [A, B]
        return SquareMatrix.Sub(SquareMatrix.Mul(A, B), SquareMatrix.Mul(B, A))
    @staticmethod
    def AntiCommutator(A, B): #Gives {A, B}
        return SquareMatrix.Add(SquareMatrix.Mul(A, B), SquareMatrix.Mul(B, A))
    @staticmethod
    def IsSymmetric(matrix):
        matrixContents = matrix.GetContent()
        for i in range(len(matrixContents)-1):
            for j in range(i + 1, len(matrixContents)):
                if(matrixContents[i][j] != matrixContents[j][i]):
                    return False
        return True
    @staticmethod
    def IsAntiSymmetric(matrix):
        matrixContents = matrix.GetContent()
        for i in range(len(matrixContents)):
            for j in range(i, len(matrixContents)):
                if(matrixContents[i][j] + matrixContents[j][i] != 0):
                    return False
        return True
    @staticmethod
    def IsOrthogonal(matrix):
        if(SquareMatrix.Det(matrix) == 0):
            return False
        return SquareMatrix.Equal(SquareMatrix.Transposed(matrix), SquareMatrix.Inversed(matrix))