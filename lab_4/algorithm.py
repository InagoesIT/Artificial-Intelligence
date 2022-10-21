from n_queens import ProblemModel


class Algorithm:
    def __init__(self, model: ProblemModel):
        self.model = model

    def get_smallest_domain(self):
        # to do: as Ina said
        best_index = -1
        best_size = 1e10
        for index, domain in enumerate(self.model.queen_domains):
            if len(domain) < best_size:
                best_size = len(domain)
                best_index = index
        return best_index
