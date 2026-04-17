#include<bits/stdc++.h>
using namespace std;
const int N=110;
int n,m,cnt;
int mp[N][N],st[N][N];
int dx[]={1,-1,0,0},dy[]={0,0,1,-1};
typedef pair<int,int> PII;
void bfs(int x,int y)
{
	queue<PII> q;
	q.push(make_pair(x,y));
	st[x][y]=1;
	while(q.size())
	{
		PII p=q.front();
		q.pop();
		int x=p.first,y=p.second;
		for(int i=0;i<4;i++)
		{
			int xx=x+dx[i],yy=y+dy[i];
			if(xx<1||x>n||y<1||y>m||st[xx][yy]||mp[xx][yy]==0) continue;
			st[xx][yy]=1;
			q.push(make_pair(xx,yy));
		}
	}
} 
int main()
{
	cin>>n>>m;
	char ch;
	for(int i=1;i<=n;i++)
		for(int j=1;j<=m;j++)
		{
			cin>>ch;
			mp[i][j]=ch-'0';
		}
	for(int i=1;i<=n;i++)
		for(int j=1;j<=m;j++)
		{
			if(mp[i][j]>0&&!st[i][j])
			{
				bfs(i,j);
				cnt++;
			}
		}
	cout<<cnt<<endl;
	return 0;		
} 