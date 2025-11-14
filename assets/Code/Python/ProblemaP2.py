import sys
"""
Proyecto parte 2
Hecho por
- Daniel Santiago Muñoz
- Juan David Ortiz
"""
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # Path compression
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False

        # Union by size
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        return True

def main():
    input = sys.stdin.read().split()
    t = int(input[0])
    idx = 1
    results = []

    for _ in range(t):
        n = int(input[idx]); idx += 1
        m = int(input[idx]); idx += 1

        dsu_fibra = DSU(n)
        dsu_coaxial = DSU(n)

        ff2c = [set() for _ in range(n)]
        cf2f = [set() for _ in range(n)]

        for i in range(n):
            ff2c[i].add(i)
            cf2f[i].add(i)

        pairs = n
        froots = n
        croots = n
        current_line = []

        for _ in range(m):
            u = int(input[idx]) - 1; idx += 1
            v = int(input[idx]) - 1; idx += 1
            k = int(input[idx]); idx += 1

            if k == 1:
                ru = dsu_fibra.find(u)
                rv = dsu_fibra.find(v)
                if ru != rv:
                    # Siempre unir el más pequeño al más grande
                    if dsu_fibra.size[ru] < dsu_fibra.size[rv]:
                        ru, rv = rv, ru

                    # Calcular intersección
                    sru, srv = ff2c[ru], ff2c[rv]

                    # Usar intersección
                    intersection = sru & srv
                    pairs -= len(intersection)

                    # Mover todos los elementos de rv a ru
                    for croot in srv:
                        ff2c[ru].add(croot)
                        cf2f[croot].discard(rv)
                        cf2f[croot].add(ru)

                    # Unir en DSU
                    dsu_fibra.union(u, v)
                    ff2c[rv].clear()
                    froots -= 1

            else:  # k == 2
                cu = dsu_coaxial.find(u)
                cv = dsu_coaxial.find(v)
                if cu != cv:
                    if dsu_coaxial.size[cu] < dsu_coaxial.size[cv]:
                        cu, cv = cv, cu

                    scu, scv = cf2f[cu], cf2f[cv]
                    intersection = scu & scv
                    pairs -= len(intersection)

                    for froot in scv:
                        cf2f[cu].add(froot)
                        ff2c[froot].discard(cv)
                        ff2c[froot].add(cu)

                    dsu_coaxial.union(u, v)
                    cf2f[cv].clear()
                    croots -= 1

            # Verificación redundante
            current_line.append('1' if (pairs == froots == croots) else '0')

        results.append(' '.join(current_line))

    print('\n'.join(results))

if __name__ == "__main__":
    main()