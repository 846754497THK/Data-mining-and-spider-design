#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int INF=0x3f3f3f3f;
int main(){
	int n=20;
	freopen("in1.txt","r",stdin);
	freopen("out2.txt","w",stdout);
	double a[30];
	for(int i=0;i<n;i++)cin>>a[i];
	double b[100]={1.0001,1.0002,1.0003,1.0004,1.0005,1.0006,1.0007,1.0008,1.0009,1.001,
				1.0011,1.0012,1.0013,1.0014,1.0015,1.0016,1.0017,1.0018,1.0019,1.002,
				1.0025,1.003,1.0035,1.004,1.005,1.006,1.007,1.008,1.009,1.01,
				1.011,1.012,1.013,1.014,1.015,1.016,1.017,1.018,1.019,1.02
				,1.025,1.03,1.035,1.04,1.045,1.05,1.06,1.07,1.08,1.09,1.1
				,1.11,1.12,1.13,1.14,1.15,1.16,1.17,1.18,1.19,1.2
				,1.25,1.3,1.35,1.4,1.45,1.5,1.6,1.7,1.8,1.9,2
				};

	for(int j=0;b[j]!=0;j++)printf("%lf\t",b[j]);

	return 0;
}
