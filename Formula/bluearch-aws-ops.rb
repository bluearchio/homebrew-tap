class BluearchAwsOps < Formula
  desc "AWS operations CLI for recommendations, alerting, and remediation"
  homepage "https://github.com/bluearchio/bluearch-aws-ops"
  url "https://github.com/bluearchio/bluearch-aws-ops/releases/download/v0.13.7/bluearch-aws-ops-macos-arm64.zip"
  version "0.13.7"
  sha256 "06821efaa125bbcfb94442188a08936912f8058e2934dffa6cd07b65905434e1"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "bluearch-aws-ops"
  end

  def caveats
    <<~EOS
      bluearch-aws-ops has been installed.

      Start Core first:
        bluearch-aws-core start --daemon

      Commands:
        bluearch-aws-ops --help

      Getting started:
        bluearch-aws-ops scan

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored in: ~/.bluearch/
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-ops", "--version"
  end
end
