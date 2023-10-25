#if defined(__clang__)
#include<cassert>
#include<cctype>
#include<climits>
#include<cmath>
#include<cstddef>
#include<cstdint>
#include<cstdio>
#include<cstdlib>
#include<cstring>
#include<ctime>

#include <array>
#include <bitset>
#include <deque>
// #include <flat_map>
// #include <flat_set>
#include <forward_list>
#include <list>
#include <map>
// #include <mdspan>
#include <queue>
#include <set>
// #include <span>
#include <stack>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include <algorithm>
#include <functional>
#include <limits>
#include <numeric>
// #include <print>
#include <utility>

using namespace std;
#elif defined(__GNUG__)
#include <bits/stdc++.h>
#include <bits/extc++.h>

using namespace std;
using namespace __gnu_pbds;
typedef tree<string, null_type, less<string>, rb_tree_tag,
        tree_order_statistics_node_update> ost;

#endif
