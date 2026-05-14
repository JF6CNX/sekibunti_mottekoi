from dataclasses import dataclass, field


@dataclass
class AppState:
    selected_samples: list = field(default_factory=list)
    sample_order_map: dict = field(default_factory=dict)
    checkbox_refs: dict = field(default_factory=dict)
    sample_groups: dict = field(default_factory=dict)
    samples_keys: list = field(default_factory=list)

    def set_sample_groups(self, sample_groups):
        self.sample_groups = sample_groups
        self.samples_keys = sorted(sample_groups.keys())

    def select_sample(self, sample_name):
        if sample_name not in self.selected_samples:
            self.selected_samples.append(sample_name)

    def unselect_sample(self, sample_name):
        if sample_name in self.selected_samples:
            self.selected_samples.remove(sample_name)

        self.sample_order_map.pop(sample_name, None)

    def clear_samples(self):
        self.selected_samples.clear()
        self.sample_order_map.clear()

        for checkbox in self.checkbox_refs.values():
            checkbox.value = False

    def toggle_number(self, sample_name, number):
        order = self.sample_order_map.setdefault(sample_name, [])

        if number in order:
            order.remove(number)
        else:
            order.append(number)

    def get_order(self, sample_name):
        return self.sample_order_map.get(sample_name, [])

    def set_order(self, sample_name, order):
        self.sample_order_map[sample_name] = list(order)
