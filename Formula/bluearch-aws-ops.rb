class BluearchAwsOps < Formula
  desc "AWS operations CLI for recommendations, alerting, and remediation"
  homepage "https://github.com/bluearchio/bluearch-aws-ops"
  url "https://dist.bluearch.io/releases/bluearch-aws-ops/v0.13.3/bluearch-aws-ops-macos-arm64.zip"
  version "v0.13.3"
  sha256 "7a3b875b53215ba382021c28bdd105433423048444489b76a516315350c7335e"
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
