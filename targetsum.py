class Solution:
    """
    @param nums: the given array
    @param s: the given target
    @return: the number of ways to assign symbols to make sum of integers equal to target S
    """

    def findTargetSumWays(self, nums, s):
        dp = [0] * (len(nums) + 1)
        for i in range(len(dp)):
            dp[i] = dict()

        dp[0][0] = 1
        for i in range(len(nums)):
            for sum in dp[i]:
                cnt = dp[i][sum]
                try:
                    dp[i + 1][sum + nums[i]] += cnt
                except KeyError:
                    dp[i + 1][sum + nums[i]] = 0
                    dp[i + 1][sum + nums[i]] += cnt
                try:
                    dp[i + 1][sum - nums[i]] += cnt
                except KeyError:
                    dp[i + 1][sum - nums[i]] = 0
                    dp[i + 1][sum - nums[i]] += cnt

        return dp[len(nums)][s]
        # return self.c

a = [1, 1, 1, 1, 1]
s = 3
sol = Solution()
print sol.findTargetSumWays(a, s)