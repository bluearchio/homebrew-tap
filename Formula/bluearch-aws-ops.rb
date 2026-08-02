class BluearchAwsOps < Formula
  desc "AWS operations CLI for recommendations, alerting, and remediation"
  homepage "https://github.com/bluearchio/bluearch-aws-ops"
  url "https://github.com/bluearchio/bluearch-aws-ops/releases/download/v0.13.6/bluearch-aws-ops-macos-arm64.zip"
  version "0.13.6"
  sha256 "e75d9707b1eac7da63c08aa6206531126d0a21f30391409e954e2ff27de456ca"
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
