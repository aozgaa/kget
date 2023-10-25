#include "bits.h"

#define range(ds) std::begin(ds), std::end(ds)

#define MAX_M (10'002)
int n,m;
string s,t;
string V[MAX_M];
vector<int> adj[MAX_M];
std::array<int, MAX_M> prevv; // doubles as visited check

int main() {
    cin >> n >> m >> s >> t;
    assert(m <= 10'000);
    for (int i = 0; i < m; ++i) {
        cin >> V[i];
    }
    int si = m;   V[si] = s;
    int ti = m+1; V[ti] = t;

    std::fill(range(prevv), -1);
    prevv[si] = si; // self-loop

    for (int i = 0; i < m+2; ++i) {
        for (int j = i+1; j < m+2; ++j) {
            int dist = 0; 
            for (int k = 0; k < n; ++k) {
                char lo = std::min(V[i][k], V[j][k]);
                char hi = std::max(V[i][k], V[j][k]);
                if (hi == lo) { continue; }
                if (hi - lo == 1 || (hi == '9' && lo == '0')) { dist++; }
                else { goto NEXT; }
            }
            if (dist != 1) { continue; }
            adj[i].push_back(j);     
            adj[j].push_back(i);
NEXT:;
        }
    }

    // bfs
    queue<int> q;
    q.push(si);
    while(!q.empty()) {
        int v = q.front(); q.pop();
        assert(v != -1);
        assert(prevv[v] != -1);

        if(V[v] == t) { // done
            stack<int> path;
            while(v != si) { path.push(v); v = prevv[v]; }
            printf("%ld\n", path.size());
            path.push(si);
            while(!path.empty()) {
                int v = path.top(); path.pop();
                printf("%s\n", V[v].c_str());
            }
            exit(0);
        }

        for (auto w : adj[v]) {
            if (prevv[w] != -1) { continue; }
            prevv[w] = v;
            q.push(w);
        }
    }
    printf("Neibb\n");

    return 0;
}
