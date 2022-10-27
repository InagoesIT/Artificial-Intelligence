class Algorithm:
    def __init__(self, model):
        self.model = model
        self.solution_found = False

    def get_queen_index_by_smallest_domain(self) -> int:
        best_index = -1
        best_size = int(1e6)
        for index, domain in enumerate(self.model.queen_domains):
            if len(domain) < best_size and self.model.queen_column[index] == -1:
                best_size = len(domain)
                best_index = index
        return best_index

    def update_domains(self, queen_index: int, column_index: int) -> list[tuple]:
        removed_values = []
        delta_coords_list = [(-1, 1), (1, 1), (-1, -1), (1, -1),  # diag coords
                             (0, 1), (0, -1), (1, 0), (-1, 0)]  # axis parallel coords

        for index in range(0, self.model.n):
            for delta_coords in delta_coords_list:
                new_line = queen_index + delta_coords[0] * index
                new_column = column_index + delta_coords[1] * index
                if 0 <= new_line <= self.model.n - 1 and 0 <= new_column <= self.model.n - 1:
                    if new_column in self.model.queen_domains[new_line]:
                        self.model.queen_domains[new_line].remove(new_column)
                        removed_values.append((new_line, new_column))
        return removed_values

    def rollback_domains(self, to_be_rolled_back: list[tuple]):
        for element in to_be_rolled_back:
            self.model.queen_domains[element[0]].add(element[1])

    def build_solution(self, queen_index: int):
        for column_index in self.model.queen_domains[queen_index]:
            self.model.queen_column[queen_index] = column_index
        self.model.pretty_print_model()
        self.model.queen_column[queen_index] = -1

    def __run__(self, queen_index: int, depth_level: int):
        if self.solution_found:
            return

        if depth_level == self.model.n and not self.solution_found:
            self.build_solution(queen_index)
            self.solution_found = True
            return

        snapshot_queen_domains = self.model.queen_domains[queen_index].copy()
        for column_index in snapshot_queen_domains:
            self.model.queen_column[queen_index] = column_index
            removed_domains = self.update_domains(queen_index=queen_index, column_index=column_index)
            next_queen = self.get_queen_index_by_smallest_domain()
            if next_queen != -1:
                self.__run__(queen_index=next_queen, depth_level=depth_level + 1)
            self.rollback_domains(removed_domains)
        self.model.queen_column[queen_index] = -1

    def run(self) -> None:
        start_queen = self.get_queen_index_by_smallest_domain()
        self.__run__(queen_index=start_queen, depth_level=1)
