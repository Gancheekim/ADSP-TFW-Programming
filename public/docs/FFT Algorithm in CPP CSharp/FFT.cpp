#include <iostream>
#include <string>
#include <vector>
#include <cmath>

using namespace std;
const float PI = 3.14159;
const float e = 2.71828182845904523536;

class Complex {
public:
    Complex() = default;
    Complex(float r_, float i_) : r(r_), i(i_) { }
    string ToString() {
        return to_string(r) + "+" + to_string(i) + "i";
    }
    Complex operator+(Complex y) {
        return Complex(r + y.r, i + y.i);
    }
    Complex operator-(Complex y) {
        return Complex(r - y.r, i - y.i);
    }
    Complex operator*(Complex y) {
        return Complex((r * y.r - i * y.i), (r * y.i + i * y.r));
    }
    static Complex Polar(double r, double radians) {
        return Complex(r * cos(radians), r * sin(radians));
    }
    float r = 0, i = 0;
};

vector<Complex> fft(vector<Complex> x) {
    int N = x.size();
    vector<Complex> X(N), odd(N/2), even(N/2), ODD, EVEN;
    if (N == 1) {
        X[0] = x[0];
        return X;
    }
    int k = 0;
    for (k = 0; k < N / 2; k++) {
        even[k] = x[2 * k];
        odd[k] = x[2 * k + 1];
    }
    ODD = fft(odd);
    EVEN = fft(even);
    for (k = 0; k < N / 2; k++){
        Complex temp = Complex::Polar(1, -2 * PI * k / N);
        ODD[k] = ODD[k] * temp;
    }
    for (k = 0; k < N / 2; k++){
        X[k] = (EVEN[k] + ODD[k]) * Complex(0.5f, 0);
        X[k + N / 2] = (EVEN[k] - ODD[k]) * Complex(0.5f, 0);
    }
    return X;
}

int main() {
    int N, M;
    cout<<"Constraint: N>2M+1, N must be 2 power"<<endl;
    cout << "Please enter the number for N=" << endl;
    cin >> N;
    cout << "Please enter the number for M=" << endl;
    cin >> M;
    vector<Complex> x(N);
    //設定Time Domain的初始值
    for (int k = 0; k < N; k++){
        if (k <= M)
        x[k] = Complex(1, 0);
        else if (k < N - M)
        x[k] = Complex(0, 0);
        else
        x[k] = Complex(1, 0);
    }
    //列印出Time Domain 和 Frequency Domain的值
    for (int k = 0; k < N; k++){
        cout << "x[" << k << "]: " << x[k].ToString()<<endl;
    }
    cout << endl;
    cout << endl;
    auto ret = fft(x);
    for (int k = 0; k < N; k++){
        cout << "X[" << k << "]: " << ret[k].ToString()<<endl;
    }
    cout << endl;
    return 0;
}