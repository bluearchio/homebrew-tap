class TagManager < Formula
  desc "AWS Tag Manager CLI - FinOps, compliance, and cost optimization tool"
  homepage "https://bluearch.io"
  version "v0.3.1"
  license :cannot_represent

  depends_on arch: :arm64

  url "https://dist.bluearch.io/tag-manager/v0.3.1/tag-manager_macos_arm64"
  sha256 "f3ff913ad4f7ae6c448e7dda85a477a63aff36fe17e05ffa620780215d86366a"

  def install
    bin.install "tag-manager_macos_arm64" => "tag-manager"
  end

  test do
    system "#{bin}/tag-manager", "--version"
  end
end
