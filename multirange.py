import bisect


class MultiRange:
    def __init__(self, ranges=[]):
        """Represent ranges by sorted lists of starts and ends,
        whose indices correspond to a range.
        I do this so that I can easily use bisect functions on them.
        I can do this because the MultiRange will should always be in the form
        (s_1, e_1), ..., (s_n, e_n); where s_i < e_i < s_i+1 < e_i+1.
        If e.g. e_1 == s_2, I can merge (s_1, e_1), (s_2, e_2) -> (s_1, e_2)
        """
        self.starts = []
        self.ends = []
        for start, end in ranges:
            self.add(start, end)

    @property
    def ranges(self):
        return list(zip(self.starts, self.ends))

    def get_intersection_bound(self, start, end):
        """Find the indices such that the ranges contained intersect with start, end.
        Complexity: O(log(n)) where n is the number of ranges
        """
        lo = bisect.bisect_right(self.ends, start)
        hi = bisect.bisect_left(self.starts, end, lo)
        return lo, hi

    def get_union_bound(self, start, end):
        """Find the indices such that the ranges contained will merge with start, end.
        This differs from get_intersection_bound in that it includes ranges
        that ends at start and starts at end.
        Complexity: O(log(n))
        """
        lo = bisect.bisect_left(self.ends, start)
        hi = bisect.bisect_right(self.starts, end, lo)
        return lo, hi

    def add(self, start, end):
        """Add range start, end.
        Complexity: O(n) due to slice assignment
        """
        assert(start < end)
        lo, hi = self.get_union_bound(start, end)
        # The affected ranges get merged into one.
        self.starts[lo:hi] = [min([start] + self.starts[lo:hi])]
        self.ends[lo:hi] = [max([end] + self.ends[lo:hi])]

    def delete(self, start, end):
        """Delete range start, end.
        Complexity: O(n) due to slice assignment
        """
        lo, hi = self.get_intersection_bound(start, end)
        if hi > lo:
            # If hi <= lo, no ranges are touched.
            # Only the ranges at lo and hi - 1 may partially intersect -
            # anything in the middle is completely consumed.
            # If start, end is contained in one range, that range splits into two.
            starts_middle = []
            ends_middle = []
            if self.starts[lo] < start < self.ends[lo]:
                starts_middle.append(self.starts[lo])
                ends_middle.append(start)

            if self.starts[hi - 1] < end < self.ends[hi - 1]:
                starts_middle.append(end)
                ends_middle.append(self.ends[hi - 1])

            self.starts[lo:hi] = starts_middle
            self.ends[lo:hi] = ends_middle

    def get(self, start, end):
        """Get the ranges that intersect with start, end.
        Complexity: O(hi - lo)
        """
        lo, hi = self.get_intersection_bound(start, end)
        return list(zip(self.starts[lo:hi], self.ends[lo:hi]))
