class BluearchAwsTags < Formula
  desc "AWS tagging, lifecycle, tag policy, and FinOps CLI"
  homepage "https://github.com/bluearchio/bluearch-aws-tags"
  url "https://dist.bluearch.io/releases/bluearch-aws-tags/v0.12.3/bluearch-aws-tags-macos-arm64.zip"
  version "v0.12.3"
  sha256 "fc8644656df517ff87b236bf6f1919de48dfa1c7482aeda9022692643b278b10"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "bluearch-aws-tags"
  end

  def caveats
    <<~EOS
      bluearch-aws-tags has been installed.

      Start Core first:
        bluearch-aws-core start --daemon

      Commands:
        bluearch-aws-tags --help

      Getting started:
        bluearch-aws-tags setup validate

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored locally by the product runtime.
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-tags", "--version"
  end
end
